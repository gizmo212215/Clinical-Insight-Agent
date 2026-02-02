import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.core.database import SessionLocal, init_db
from backend.services.ingestion.processor import IngestionPipeline
from backend.core.logger import get_logger
import time

logger = get_logger("script_bulk_ingest")


def main():
    logger.info("🚀 Batch Data Ingestion Script Started.")
    try:
        init_db()
        logger.info("✅ Database tables checked/created.")
    except Exception as e:
        logger.critical(f"❌ Database initialization failed: {e}")
        return

    db = SessionLocal()
    pipeline = IngestionPipeline(db)
    conditions = ["Lung Cancer", "Diabetes", "Alzheimer", "Hypertension"]

    try:
        for condition in conditions:
            logger.info(f"📥 Processing condition: '{condition}'")
            pipeline.run(condition=condition, limit=10)
            logger.info("⏳ Waiting 2 seconds to respect API limits...")
            time.sleep(2)

        logger.info("🎉 ALL TASKS COMPLETED SUCCESSFULLY.")

    except KeyboardInterrupt:
        logger.warning("⚠️ Process interrupted by user (Ctrl+C).")
    except Exception as e:
        logger.error(f"❌ Unexpected Error: {e}", exc_info=True)
    finally:
        db.close()
        logger.info("🔌 Database connection closed.")


if __name__ == "__main__":
    main()
