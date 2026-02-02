from datetime import datetime
from sqlalchemy.orm import Session
from backend.core.logger import get_logger
from backend.models.sql_models import ClinicalTrial
from backend.services.ingestion.client import ClinicalTrialsClient
from backend.services.rag_engine.vector_store import VectorDBManager

logger = get_logger("ingestion_processor")


class IngestionPipeline:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.api_client = ClinicalTrialsClient()
        try:
            self.vector_manager = VectorDBManager()
        except Exception as e:
            logger.critical(
                f"❌ Failed to initialize VectorDBManager: {e}", exc_info=True
            )
            raise e

    def run(self, condition: str, limit: int = 10):
        logger.info(
            f"🚀 Starting ingestion pipeline for '{condition}' (Limit: {limit})..."
        )
        raw_studies = self.api_client.fetch_studies(condition, limit)
        if not raw_studies:
            logger.warning(f"⚠️ No studies found for '{condition}'. Aborting pipeline.")
            return

        sql_objects = []
        vector_texts = []
        vector_metadatas = []
        logger.info(f"🔄 Transforming {len(raw_studies)} raw records...")

        for study in raw_studies:
            try:
                protocol = study.get("protocolSection", {})
                identification = protocol.get("identificationModule", {})
                status_mod = protocol.get("statusModule", {})
                design = protocol.get("designModule", {})
                nct_id = identification.get("nctId")
                if not nct_id:
                    logger.debug("Skipping record without NCT ID.")
                    continue
                start_date_str = status_mod.get("startDateStruct", {}).get("date")
                start_date = None
                if start_date_str:
                    try:
                        if len(start_date_str) > 7:
                            start_date = datetime.strptime(
                                start_date_str, "%Y-%m-%d"
                            ).date()
                        elif len(start_date_str) == 7:
                            start_date = datetime.strptime(
                                start_date_str, "%Y-%m"
                            ).date()
                    except ValueError:
                        logger.debug(
                            f"Date parsing failed for {nct_id} ({start_date_str}), setting None."
                        )
                        start_date = None

                phases = ", ".join(design.get("phases", []))
                title = identification.get("briefTitle", "")[:3000]

                trial_obj = ClinicalTrial(
                    nct_id=nct_id,
                    title=title,
                    organization=protocol.get("identificationModule", {})
                    .get("organization", {})
                    .get("fullName"),
                    status=status_mod.get("overallStatus"),
                    phases=phases,
                    study_type=design.get("studyType"),
                    start_date=start_date,
                )
                sql_objects.append(trial_obj)
                desc_mod = protocol.get("descriptionModule", {})
                eligibility = protocol.get("eligibilityModule", {})

                full_text = f"""
                TRIAL ID: {nct_id}
                TITLE: {title}
                STATUS: {status_mod.get("overallStatus")}
                PHASE: {phases}
                SUMMARY:
                {desc_mod.get("briefSummary", "")}
                ELIGIBILITY CRITERIA:
                {eligibility.get("eligibilityCriteria", "")}
                """

                vector_texts.append(full_text)
                vector_metadatas.append({"nct_id": nct_id, "title": title})

            except Exception as e:
                logger.error(
                    f"❌ Error processing record {nct_id if 'nct_id' in locals() else 'Unknown'}: {e}"
                )
                continue

        if sql_objects:
            try:
                logger.info(f"💾 Saving {len(sql_objects)} records to SQL Database...")
                for obj in sql_objects:
                    self.db.merge(obj)
                self.db.commit()
                logger.info("✅ SQL save successful.")
            except Exception as e:
                self.db.rollback()
                logger.error(f"❌ SQL Database Error: {e}", exc_info=True)

        if vector_texts:
            try:
                logger.info(
                    f"🧠 Generating embeddings and saving to Vector DB ({len(vector_texts)} docs)..."
                )
                self.vector_manager.add_texts(vector_texts, vector_metadatas)
                logger.info("✅ Vector DB save successful.")
            except Exception as e:
                logger.error(f"❌ Vector DB Error: {e}", exc_info=True)

        logger.info(f"🎉 Pipeline finished for '{condition}'.")
