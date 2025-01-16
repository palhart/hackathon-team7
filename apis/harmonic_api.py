# harmonic_api.py
import requests
from loguru import logger

class HarmonicAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.harmonic.ai"

    def post_companies(self, website_domain):
        endpoint = f"{self.base_url}/companies"
        params = {
            "website_domain": website_domain,
        }
        return self._send_request("POST", endpoint, params=params)

    def get_similar_companies(self, urn, size=15):
        endpoint = f"{self.base_url}/search/similar_companies/{urn}"
        params = {
            "size": size,
        }
        return self._send_request("GET", endpoint, params=params)

    def get_user_connections(self, urn):
        endpoint = f"{self.base_url}/companies/{urn}/userConnections"
        return self._send_request("GET", endpoint)

    def get_company_details(self, urn):
        logger.info(urn)
        endpoint = f"{self.base_url}/companies/{urn}"
        return self._send_request("GET", endpoint)

    def get_company_employees(self, urn):
        endpoint = f"{self.base_url}/companies/{urn}/employees"
        return self._send_request("GET", endpoint)

    def _send_request(self, method, endpoint, params=None):
        headers = {
            "accept": "application/json", 
            "apikey": self.api_key
        }
        if method == "POST":
            response = requests.post(endpoint, params=params, headers=headers)
        else:
            response = requests.get(endpoint, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
