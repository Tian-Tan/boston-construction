from django.shortcuts import render, loader, get_object_or_404
from django.http import HttpResponse
from django.core import serializers
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from boston_construction.models import MailingListRecord, ConstructionRecord
from django.template.loader import render_to_string
from django.utils.safestring import SafeString
import requests
import string
import random
from django.contrib.messages.views import SuccessMessageMixin
import re
from django.utils.dateparse import parse_datetime
from django.utils import timezone

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-Postmark-Server-Token": "f906c1c8-aab3-4506-843b-be25abc74afa"
}

def index(request):
    works = ConstructionRecord.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True).filter(expiration_date__gt=timezone.now())
    works_json = serializers.serialize('json', works)
    template = loader.get_template('index.html')
    context = {
        'worklist': SafeString(works_json),
    }
    return HttpResponse(template.render(context, request))

def aboutus(request):
    template = loader.get_template('boston_construction/aboutus.html')
    context = {}
    return HttpResponse(template.render(context, request))

class MailingListRecordCreateView(CreateView, SuccessMessageMixin):
    model = MailingListRecord
    fields = ["email", "zip_code"]
    success_url = "http://127.0.0.1:8000/app/mailing-list"
    success_message = "Succesfully signed up!"

    def form_invalid(self, form):
        return self.render_to_response({"message": "Failed to sign up! Are you already signed up?"})

    def form_valid(self, form):
        form.instance.secret = ''.join(random.choices(string.ascii_uppercase + string.digits, k=64))
        self.object = form.save()
        return self.render_to_response({"message": "Successfully signed up!"})

def delete_email(request, secret):
    record = get_object_or_404(MailingListRecord, secret=secret)
    record.delete()
    return render(request, "boston_construction/deleted_email.html", {"email": record.email})

def send_email(request):
    """
    DEVELOPMENT ROUTE! Send a GET here to send emails to subscribers.
    """
    mail_records = MailingListRecord.objects.all()
    for mail_record in mail_records:
        construction = ConstructionRecord.objects.filter(zip_code=mail_record.zip_code).filter(expiration_date__gt=timezone.now()).values()
        print(construction)
        email_body = render_to_string("boston_construction/email.html", {"construction": construction})
        data = {
            "From": "belyaev.l@northeastern.edu",
            "To": f"{mail_record.email}",
            "Subject": "Daily BCWerk Notification",
            "HtmlBody": email_body,
            "MessageStream": "outbound"
        }
        response = requests.post("https://api.postmarkapp.com/email", headers=headers, json=data)

def get_data(request):
    # TODO is there a more generic way to refer to this, so that it's the one updated daily?
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
