from django.apps import AppConfig
import requests

class BostonConstructionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "boston_construction"

    def ready(self):
        """
        Django runs this code on app startup
        """

        # Sets a task runner schedule!!

        # TODO is there a more generic way to refer to this, so that it's the one updated daily?
        response = requests.get(f"https://data.boston.gov/api/3/action/datastore_search?offset=0&resource_id=36fcf981-e414-4891-93ea-f5905cec46fc")
        data_json = response.json()
        total = data_json["result"]["total"]
        print(f"Total is {total}")
        records = []
        while len(records) != total:
            response = requests.get(f"https://data.boston.gov/api/3/action/datastore_search?offset={len(records)}&resource_id=36fcf981-e414-4891-93ea-f5905cec46fc")
            records += response.json()["result"]["records"]
            print(f"Got {len(records)} objects")
