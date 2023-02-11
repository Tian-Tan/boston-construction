from django.apps import AppConfig

# TODO is there a more generic way to refer to this, so that it's the one updated daily?
DATA_URL = "https://data.boston.gov/api/3/action/datastore_search?offset={offset}&resource_id=36fcf981-e414-4891-93ea-f5905cec46fc"


class BostonConstructionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "boston_construction"

    def ready(self):
        """
        Django runs this code on app startup
        """
        # TODO get data
