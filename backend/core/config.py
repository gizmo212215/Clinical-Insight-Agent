import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = "Clinical Insight Agent"
    VERSION: str = "1.0.0"
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql://admin:password123@localhost:5432/clinical_trials"
    )
    CHROMA_PERSIST_DIR: str = os.getenv("CHROMA_PERSIST_DIRECTORY", "./data/chroma_db")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    LOG_DIR: str = "./data/raw_logs"
    LOG_FILE: str = os.path.join(LOG_DIR, "agent.log")


settings = Settings()
