from django.apps import AppConfig

# TODO is there a more generic way to refer to this, so that it's the one updated daily?


class BostonConstructionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "boston_construction"

    def ready(self):
        """
        Django runs this code on app startup
        """
        offset = 0
        response = requests.get(f"https://data.boston.gov/api/3/action/datastore_search?offset={offset}&resource_id=36fcf981-e414-4891-93ea-f5905cec46fc")
        data_txt = response.text # TODO do we need to index a particular json point?
        while response.status_code == 200:
            offset += 100 #loltacular code
            response = requests.get(f"https://data.boston.gov/api/3/action/datastore_search?offset={offset}&resource_id=36fcf981-e414-4891-93ea-f5905cec46fc")
            data_txt += response.text

        # TODO get data
