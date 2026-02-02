import requests
from typing import List, Dict, Any
from backend.core.logger import get_logger

t
logger = get_logger("api_client")


class ClinicalTrialsClient:
    BASE_URL = "https://clinicaltrials.gov/api/v2/studies"

    def fetch_studies(
        self, condition: str = None, page_size: int = 10
    ) -> List[Dict[str, Any]]:
        params = {
            "pageSize": page_size,
            "fields": "NCTId,BriefTitle,BriefSummary,DetailedDescription,EligibilityModule,ConditionsModule,Phase,StatusModule,DesignModule",
        }

        if condition:
            params["query.cond"] = condition

        try:
            logger.info(
                f"🌐 Sending API Request for condition: '{condition}' (Limit: {page_size})..."
            )
            response = requests.get(self.BASE_URL, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            studies = data.get("studies", [])
            count = len(studies)
            if count == 0:
                logger.warning(f"⚠️ API returned 0 results for condition: '{condition}'")
            else:
                logger.info(f"✅ Successfully fetched {count} studies.")

            return studies

        except requests.exceptions.Timeout:
            logger.error(
                f"❌ API Timeout Error: The request took too long for '{condition}'.",
                exc_info=True,
            )
            return []

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ API Connection Error: {str(e)}", exc_info=True)
            return []

        except Exception as e:
            logger.error(f"❌ Unexpected Error during fetch: {str(e)}", exc_info=True)
            return []
