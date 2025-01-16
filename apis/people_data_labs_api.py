from peopledatalabs import PDLPY
import json

class PeopleDataLabsAPI:
    def __init__(self, api_key):
        self.client = PDLPY(api_key=api_key)

    def company_enrichment(self, website):
        query_string = {"website": website}
        response = self.client.company.enrichment(**query_string).json()
        return response

    def company_search(self, website, size=10, pretty=True):
        es_query = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"website": website}},
                    ]
                }
            }
        }
        params = {
            'query': es_query,
            'size': size,
            'pretty': pretty
        }
        response = self.client.company.search(**params).json()

        return response

        