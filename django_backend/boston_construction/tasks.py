import requests
from .models import MailingListRecord, ConstructionRecord
from django.template.loader import render_to_string
import django

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-Postmark-Server-Token": "f906c1c8-aab3-4506-843b-be25abc74afa"
}

django.setup()

def send_emails():
    mail_records = MailingListRecord.objects.all()
    for mail_record in mail_records:
        construction = ConstructionRecord.objects.filter(zip_code=mail_record.zip_code)
        email_body = render_to_string("email.html", construction)
        data = {
            "From": "belyaev.l@northeastern.edu",
            "To": f"{mail_record.email}",
            "Subject": "Daily BCWerk Notification",
            "HtmlBody": email_body,
            "MessageStream": "outbound"
        }
        response = requests.post("https://api.postmarkapp.com/email", headers=headers, json=data)

def get_data():
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

    # Creates models for every record, gets their location, and save them into the database
    for record in records:
        work = ConstructionRecord(_id=record['_id'], neighborhood=record['Neighborhood'], street=record['Street'], address_1=record['Address_1'],
                address_2=record['Address_2'], intersection=record['Intersection'], start=record['From'], to=record['To'], permittee=record['Permittee'],
                contractor=record['Contractor'], permit=record['Permit'], project_category=record['Project_Category'], construction_notes=record['Construction_Notes'],
                work_schedule=record['Work_Schedule'], expiration_date=record['ExpirationDate'], estimated_completion_date=record['Estimated_Completion_Date'],
                roadway_plates_in_use=record['Roadway_Plates_In_Use'], sidewalk_plates_in_use=record['Sidewalk_Plates_In_Use'], status=record['Status'],
                trench_length=record['Trench_Length'], contact_number=record['Contact_Number'], number_of_works=record['NumberOfWorkZones'],
                district=record['District'], lat=0.0, _long=0.0)
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
        work.long = data["features"][0]["geometry"]["coordinates"][1]
        work.lat = data["features"][0]["geometry"]["coordinates"][0]
        work.save()
