from typing import List, Dict
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from backend.core.config import settings
from backend.core.logger import get_logger
from backend.services.rag_engine.embeddings import get_embedding_model

logger = get_logger("vector_store")


class VectorDBManager:
    def __init__(self):
        self.embedding_fn = get_embedding_model()
        logger.info(f"📂 Initializing ChromaDB at: {settings.CHROMA_PERSIST_DIR}")

        try:
            self.vector_store = Chroma(
                persist_directory=settings.CHROMA_PERSIST_DIR,
                embedding_function=self.embedding_fn,
                collection_name="clinical_trials_collection",
            )
            logger.info("✅ ChromaDB connection established.")
        except Exception as e:
            logger.critical(f"❌ Failed to connect to ChromaDB: {e}", exc_info=True)
            raise e

    def add_texts(self, texts: List[str], metadatas: List[Dict]):
        if not texts:
            logger.warning("⚠️ No texts provided to add_texts. Skipping.")
            return

        logger.info(f"🔄 Processing {len(texts)} documents for vectorization...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )

        documents = []
        for text, meta in zip(texts, metadatas):
            chunks = text_splitter.split_text(text)
            for chunk in chunks:
                documents.append(Document(page_content=chunk, metadata=meta))

        if documents:
            try:
                logger.info(f"💾 Adding {len(documents)} text chunks to Vector DB...")
                self.vector_store.add_documents(documents)
                logger.info("✅ Documents added successfully.")
            except Exception as e:
                logger.error(
                    f"❌ Error adding documents to ChromaDB: {e}", exc_info=True
                )
        else:
            logger.warning("⚠️ Text splitting resulted in 0 documents.")

    def as_retriever(self):
        logger.debug("Returning Vector Store as Retriever.")
        return self.vector_store.as_retriever(search_kwargs={"k": 3})
