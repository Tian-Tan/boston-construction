
import requests
import re
from .models import MailingListRecord, ConstructionRecord
from django.utils.dateparse import parse_datetime

def get_data():
    response = requests.get(f"https://data.boston.gov/api/3/action/datastore_search?offset=0&resource_id=36fcf981-e414-4891-93ea-f5905cec46fc")
    data_json = response.json()
    total = data_json["result"]["total"]
    print(f"Total is {total}")
    records = data_json["result"]["records"]
    while len(records) != total:
        response = requests.get(f"https://data.boston.gov/api/3/action/datastore_search?offset={len(records)}&resource_id=36fcf981-e414-4891-93ea-f5905cec46fc")
        records += response.json()["result"]["records"]
        print(f"Got {len(records)} objects")

    # Creates models for every record, gets their location, and save them into the database
    for record in records:
        try:
            expiration_date=parse_datetime(record['ExpirationDate'])
        except TypeError:
            expiration_date = None

        try:
            estimated_completion_date=parse_datetime(record['Estimated_Completion_Date'])
        except TypeError:
            estimated_completion_date = None

        work = ConstructionRecord(_id=record['_id'], neighborhood=record['Neighborhood'], street=record['Street'], address_1=record['Address_1'],
                address_2=record['Address_2'], intersection=record['Intersection'], start=record['From'], to=record['To'], permittee=record['Permittee'],
                contractor=record['Contractor'], permit=record['Permit'], project_category=record['Project_Category'], construction_notes=record['Construction_Notes'],
                work_schedule=record['Work_Schedule'], expiration_date=expiration_date, estimated_completion_date=estimated_completion_date,
                roadway_plates_in_use=record['Roadway_Plates_In_Use'], sidewalk_plates_in_use=record['Sidewalk_Plates_In_Use'], status=record['Status'],
                trench_length=record['Trench_Length'], contact_number=record['Contact_Number'], number_of_works=record['NumberOfWorkZones'],
                                  district=record['District'], latitude=None, longitude=None, zip_code=None)
        work.save()

        # gets their location
        address = str(work.address_1)
        street = str(work.street)
        street = street.split()
        for word in street:
            address = address + "+" + word
        url = f"https://nominatim.openstreetmap.org/search?q={address}+boston&format=geojson"
        response = requests.get(url)
        data = response.json()
        try:
            work.longitude = data["features"][0]["geometry"]["coordinates"][0]
            work.latitude = data["features"][0]["geometry"]["coordinates"][1]
            full_address = data["features"][0]["properties"]["display_name"]
            print(f"{full_address}")
        except IndexError:
            continue
        rgx = re.search("\d\d\d\d\d", full_address)
        if rgx is not None:
            work.zip_code = rgx.group()
            print(f"{rgx.group()}")
        work.save()

    print("Done updating db")
