import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.core.config import settings
from backend.core.logger import get_logger
import requests

logger = get_logger("script_system_check")


def check_google_api():
    key = settings.GOOGLE_API_KEY
    if not key:
        logger.error("❌ GOOGLE_API_KEY is missing in .env file!")
        return False

    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            logger.info("✅ Google Gemini API Connection: OK")
            return True
        else:
            logger.error(
                f"❌ Google API Error: {response.status_code} - {response.text}"
            )
            return False
    except Exception as e:
        logger.error(f"❌ Google API Connection Failed: {e}")
        return False


def main():
    logger.info("🕵️ Starting System Diagnostic...")
    logger.info(f"📂 Project Name: {settings.PROJECT_NAME}")
    logger.info(f"📂 Log Directory: {settings.LOG_DIR}")

    if "postgresql" in settings.DATABASE_URL:
        logger.info("🗄️ Database Mode: PostgreSQL")
    else:
        logger.info("🗄️ Database Mode: SQLite/Other")

    check_google_api()
    logger.info("🏁 Diagnostic finished.")


if __name__ == "__main__":
    main()
