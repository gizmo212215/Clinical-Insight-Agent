from langchain_core.tools import tool
from backend.services.rag_engine.vector_store import VectorDBManager
from backend.core.database import engine
from backend.core.logger import get_logger
import pandas as pd

logger = get_logger("agent_tools")


try:
    vector_db = VectorDBManager()
    logger.info("✅ VectorDB Manager initialized for tools.")
except Exception as e:
    logger.critical(f"❌ Failed to initialize VectorDB in tools: {e}", exc_info=True)
    raise e


@tool
def search_clinical_documents(query: str) -> str:
    logger.info(f"🔍 Vector Search Tool Triggered. Query: '{query}'")

    try:
        retriever = vector_db.as_retriever()
        docs = retriever.invoke(query)
        count = len(docs)
        if count == 0:
            logger.warning(f"⚠️ No documents found for query: '{query}'")
            return "No relevant documents found."

        logger.info(f"✅ Found {count} relevant documents.")
        result = "\n\n".join(
            [f"Document {i + 1}:\n{doc.page_content}" for i, doc in enumerate(docs)]
        )
        return result

    except Exception as e:
        logger.error(f"❌ Vector Search Error: {str(e)}", exc_info=True)
        return f"Vector search error: {str(e)}"


@tool
def query_clinical_sql(query: str) -> str:
    logger.info(f"📊 SQL Tool Triggered. Query: '{query}'")

    try:
        forbidden_keywords = ["drop", "delete", "update", "insert", "alter", "truncate"]
        if any(keyword in query.lower() for keyword in forbidden_keywords):
            logger.warning(f"🚫 Security Alert: Blocked destructive query: '{query}'")
            return "ERROR: You are only allowed to execute READ-ONLY (SELECT) queries."

        with engine.connect() as connection:
            df = pd.read_sql(query, connection)

            if df.empty:
                logger.info("ℹ️ SQL Query executed but returned no results.")
                return "Query returned no results."

            row_count = len(df)
            logger.info(f"✅ SQL Query successful. Returned {row_count} rows.")
            if row_count > 20:
                logger.info(
                    f"⚠️ Result too large ({row_count} rows), truncating to top 20."
                )
                df = df.head(20)

            return df.to_markdown(index=False)

    except Exception as e:
        logger.error(f"❌ SQL Execution Error: {str(e)}", exc_info=True)
        return f"SQL Error: {str(e)}"
