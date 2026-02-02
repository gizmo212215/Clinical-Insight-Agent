from langchain_huggingface import HuggingFaceEmbeddings
from backend.core.config import settings
from backend.core.logger import get_logger

logger = get_logger("embeddings_core")


def get_embedding_model():
    model_name = settings.EMBEDDING_MODEL_NAME
    logger.info(f"📡 Loading Embedding Model: {model_name}")

    try:
        embeddings = HuggingFaceEmbeddings(
            model_name=model_name, model_kwargs={"device": "cpu"}
        )
        logger.info("✅ Embedding Model loaded successfully.")
        return embeddings
    except Exception as e:
        logger.critical(
            f"❌ Failed to load Embedding Model ({model_name}): {e}", exc_info=True
        )
        raise e
