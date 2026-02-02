import requests
import os
from backend.core.logger import get_logger

logger = get_logger("frontend_client")


class AgentClient:
    def __init__(self, base_url: str = None):
        if base_url is None:
            self.base_url = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
        else:
            self.base_url = base_url

        logger.info(f"🔌 API Client initialized. Target: {self.base_url}")

    def is_alive(self) -> bool:
        url = f"{self.base_url}/api/"
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                logger.debug("✅ Backend health check passed.")
                return True
            else:
                logger.warning(
                    f"⚠️ Backend returned status code: {response.status_code}"
                )
                return False
        except requests.exceptions.ConnectionError:
            logger.error("❌ Could not connect to Backend. Is it running?")
            return False
        except Exception as e:
            logger.error(f"❌ Health check failed: {e}")
            return False

    def get_answer(self, question: str) -> str:
        url = f"{self.base_url}/api/chat"
        payload = {"question": question}
        logger.info(f"📤 Sending question to Agent: '{question}'")
        try:
            response = requests.post(url, json=payload, timeout=60)
            if response.status_code == 200:
                data = response.json()
                answer = data.get("answer", "No answer content received.")
                logger.info("✅ Response received from Agent.")
                return answer
            else:
                error_msg = f"Backend Error ({response.status_code}): {response.text}"
                logger.error(f"❌ {error_msg}")
                return f"Error: {error_msg}"

        except requests.exceptions.Timeout:
            logger.error("❌ Request timed out (60s). Agent took too long to respond.")
            return (
                "Error: The request timed out. The agent is taking too long to think."
            )

        except Exception as e:
            logger.error(f"❌ Connection Error: {str(e)}", exc_info=True)
            return f"Connection Error: {str(e)}"
