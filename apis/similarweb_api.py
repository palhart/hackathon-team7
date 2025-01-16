# similarweb_api.py
import requests

class SimilarWebAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url_v1 = "https://api.similarweb.com/v1/website"
        self.base_url_v4 = "https://api.similarweb.com/v4/website"

    def get_total_traffic_and_engagement_visits(self, domain, start_date, end_date, main_domain_only=False):
        endpoint = f"{self.base_url_v1}/{domain}/total-traffic-and-engagement/visits"
        params = {
            "api_key": self.api_key,
            "start_date": start_date,
            "end_date": end_date,
            "main_domain_only": str(main_domain_only).lower()
        }
        return self._send_request(endpoint, params)

    def get_average_visit_duration(self, domain, start_date, end_date, main_domain_only=False):
        endpoint = f"{self.base_url_v1}/{domain}/total-traffic-and-engagement/average-visit-duration"
        params = {
            "api_key": self.api_key,
            "start_date": start_date,
            "end_date": end_date,
            "main_domain_only": str(main_domain_only).lower()
        }
        return self._send_request(endpoint, params)

    def get_bounce_rate(self, domain, start_date, end_date, main_domain_only=False):
        endpoint = f"{self.base_url_v1}/{domain}/total-traffic-and-engagement/bounce-rate"
        params = {
            "api_key": self.api_key,
            "start_date": start_date,
            "end_date": end_date,
            "main_domain_only": str(main_domain_only).lower()
        }
        return self._send_request(endpoint, params)

    def get_page_views(self, domain, start_date, end_date, main_domain_only=False):
        endpoint = f"{self.base_url_v1}/{domain}/total-traffic-and-engagement/page-views"
        params = {
            "api_key": self.api_key,
            "start_date": start_date,
            "end_date": end_date,
            "main_domain_only": str(main_domain_only).lower()
        }
        return self._send_request(endpoint, params)

    def get_global_rank(self, domain):
        endpoint = f"{self.base_url_v1}/{domain}/global-rank/global-rank"
        params = {"api_key": self.api_key}
        return self._send_request(endpoint, params)

    def get_country_rank(self, domain):
        endpoint = f"{self.base_url_v1}/{domain}/country-rank/country-rank"
        params = {"api_key": self.api_key}
        return self._send_request(endpoint, params)

    def get_category_rank(self, domain):
        endpoint = f"{self.base_url_v1}/{domain}/category-rank/category-rank"
        params = {"api_key": self.api_key}
        return self._send_request(endpoint, params)

    def get_total_traffic_by_country(self, domain):
        endpoint = f"{self.base_url_v4}/{domain}/geo/total-traffic-by-country"
        params = {"api_key": self.api_key}
        return self._send_request(endpoint, params)

    def get_demographics_groups(self, domain):
        endpoint = f"{self.base_url_v4}/{domain}/demographics_v2/groups"
        params = {"api_key": self.api_key}
        return self._send_request(endpoint, params)

    def get_demographics_age(self, domain):
        endpoint = f"{self.base_url_v4}/{domain}/demographics_v2/age"
        params = {"api_key": self.api_key}
        return self._send_request(endpoint, params)

    def get_demographics_gender(self, domain):
        endpoint = f"{self.base_url_v4}/{domain}/demographics_v2/gender"
        params = {"api_key": self.api_key}
        return self._send_request(endpoint, params)

    def get_total_audience_interests(self, domain):
        endpoint = f"{self.base_url_v4}/{domain}/total-audience-interests/also-visited"
        params = {"api_key": self.api_key}
        return self._send_request(endpoint, params)

    def get_lead_enrichment(self, domain):
        endpoint = f"{self.base_url_v1}/{domain}/lead-enrichment/all"
        params = {"api_key": self.api_key}
        return self._send_request(endpoint, params)

    def _send_request(self, endpoint, params):
        response = requests.get(endpoint, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
