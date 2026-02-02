import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from backend.models.sql_models import Base
from backend.core.logger import get_logger

load_dotenv()

logger = get_logger("database_core")
DATABASE_URL = os.getenv("DATABASE_URL")

try:
    engine = create_engine(DATABASE_URL)
    logger.info("✅ Database engine created successfully.")
except Exception as e:
    logger.critical(f"❌ Failed to create database engine: {e}", exc_info=True)
    raise e

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    logger.info("🔄 Initializing database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tables created successfully!")
    except Exception as e:
        logger.error(f"❌ Error creating tables: {e}", exc_info=True)
        raise e


def get_db():
    db = SessionLocal()
    try:
        logger.debug("Database session opened.")
        yield db
    except Exception as e:
        logger.error(f"❌ Database session error: {e}", exc_info=True)
        raise e
    finally:
        db.close()
        logger.debug("Database session closed.")
