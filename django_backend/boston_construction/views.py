from django.shortcuts import render, loader, get_object_or_404
from django.http import HttpResponse
from django.core import serializers
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from boston_construction.models import MailingListRecord, ConstructionRecord
from django.utils.safestring import SafeString
import requests
import string
import random
from django.contrib.messages.views import SuccessMessageMixin


def index(request):
    works = ConstructionRecord.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True)
    works_json = serializers.serialize('json', works)
    template = loader.get_template('index.html')
    context = {
        'worklist': SafeString(works_json),
    }
    return HttpResponse(template.render(context, request))

class MailingListRecordCreateView(CreateView, SuccessMessageMixin):
    model = MailingListRecord
    fields = ["email", "zip_code"]
    success_url = "http://127.0.0.1:8000/app/mailing-list"
    success_message = "Succesfully signed up!"

    def form_valid(self, form):
        form.instance.secret = ''.join(random.choices(string.ascii_uppercase + string.digits, k=64))
        return super(MailingListRecordCreateView, self).form_valid(form)

def delete_email(request, secret):
    record = get_object_or_404(MailingListRecord, secret=secret)
    record.delete()
    return render(request, "boston_construction/deleted_email.html", {"email": record.email})

def get_data(request):
    # TODO is there a more generic way to refer to this, so that it's the one updated daily?
    response = requests.get(f"https://data.boston.gov/api/3/action/datastore_search?offset=0&resource_id=36fcf981-e414-4891-93ea-f5905cec46fc&limit=50")
    data_json = response.json()
    total = data_json["result"]["total"]
    print(f"Total is {total}")
    records = data_json["result"]["records"]
    # while len(records) != total:
    #     response = requests.get(f"https://data.boston.gov/api/3/action/datastore_search?offset={len(records)}&resource_id=36fcf981-e414-4891-93ea-f5905cec46fc")
    #     records += response.json()["result"]["records"]
    #     print(f"Got {len(records)} objects")

    # Creates models for every record, gets their location, and save them into the database
    for record in records:
        work = ConstructionRecord(_id=record['_id'], neighborhood=record['Neighborhood'], street=record['Street'], address_1=record['Address_1'],
                address_2=record['Address_2'], intersection=record['Intersection'], start=record['From'], to=record['To'], permittee=record['Permittee'],
                contractor=record['Contractor'], permit=record['Permit'], project_category=record['Project_Category'], construction_notes=record['Construction_Notes'],
                work_schedule=record['Work_Schedule'], expiration_date=record['ExpirationDate'], estimated_completion_date=record['Estimated_Completion_Date'],
                roadway_plates_in_use=record['Roadway_Plates_In_Use'], sidewalk_plates_in_use=record['Sidewalk_Plates_In_Use'], status=record['Status'],
                trench_length=record['Trench_Length'], contact_number=record['Contact_Number'], number_of_works=record['NumberOfWorkZones'],
                                  district=record['District'], latitude=None, longitude=None)
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
        except IndexError:
            continue
        work.save()

    print("Done updating db")
