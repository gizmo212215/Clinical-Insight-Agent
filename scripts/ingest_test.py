import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.core.database import SessionLocal, init_db
from backend.services.ingestion.processor import IngestionPipeline
from backend.core.logger import get_logger

logger = get_logger("script_manual_test")


def main():
    logger.info("🧪 Manual Ingestion Test Script Started.")

    try:
        logger.info("1. Checking database tables...")
        init_db()
    except Exception as e:
        logger.critical(f"❌ Database initialization failed: {e}", exc_info=True)
        return

    logger.info("2. Opening database session...")
    db = SessionLocal()

    try:
        logger.info("3. Initializing Ingestion Pipeline...")
        pipeline = IngestionPipeline(db)
        test_condition = "Diabetes"
        test_limit = 3
        logger.info(f"4. Fetching data for '{test_condition}' (Limit: {test_limit})...")
        pipeline.run(condition=test_condition, limit=test_limit)

        logger.info("✅ TEST SUCCESSFUL: Data saved to SQL and Vector DB.")

    except Exception as e:
        logger.error(f"❌ TEST FAILED: {e}", exc_info=True)
    finally:
        db.close()
        logger.info("🔌 Database session closed.")


if __name__ == "__main__":
    main()
