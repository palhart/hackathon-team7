import requests

class PredictLeadsAPI:
    def __init__(self, api_key, api_token):
        self.api_key = api_key
        self.api_token = api_token
        self.base_url = "https://predictleads.com/api/v3/companies"

    def get_company_details(self, domain):
        endpoint = f"{self.base_url}/{domain}"
        return self._send_request(endpoint)

    def get_financing_events(self, domain):
        endpoint = f"{self.base_url}/{domain}/financing_events"
        return self._send_request(endpoint)

    def get_job_openings(self, domain):
        endpoint = f"{self.base_url}/{domain}/job_openings"
        return self._send_request(endpoint)

    def get_technology_detections(self, domain):
        endpoint = f"{self.base_url}/{domain}/technology_detections"
        return self._send_request(endpoint)

    def get_news_events(self, domain):
        endpoint = f"{self.base_url}/{domain}/news_events"
        return self._send_request(endpoint)

    def get_connections(self, domain):
        endpoint = f"{self.base_url}/{domain}/connections"
        return self._send_request(endpoint)

    def get_website_evolution(self, domain):
        endpoint = f"{self.base_url}/{domain}/website_evolution"
        return self._send_request(endpoint)

    def get_github_repositories(self, domain):
        endpoint = f"{self.base_url}/{domain}/github_repositories"
        return self._send_request(endpoint)

    def _send_request(self, endpoint):
        headers = {
            "X-Api-Key": self.api_key,
            "X-Api-Token": self.api_token
        }
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
