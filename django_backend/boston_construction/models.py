from django.db import models
from django.urls import reverse


# Create your models here.
class ConstructionRecord(models.Model):
    """
    Model for construction data, as pulled directly from data.boston.gov
    https://data.boston.gov/dataset/public-works-active-work-zones/resource/36fcf981-e414-4891-93ea-f5905cec46fc
    """
    _id = models.IntegerField() # "1"
    neighborhood = models.CharField(max_length=100, blank=True, null=True) # "ROXBURY"
    street = models.CharField(max_length=100, blank=True, null=True) # "FALCON ST"
    address_1 = models.IntegerField(blank=True, null=True) # "3"
    address_2 = models.IntegerField(blank=True, null=True) # "4"
    intersection = models.CharField(max_length=100, blank=True, null=True) # "BOYLSTON ST"
    start = models.CharField(max_length=100, blank=True, null=True) # "DUDLEY ST"
    to = models.CharField(max_length=100, blank=True, null=True) #"WINTHROP ST"
    permittee = models.CharField(max_length=200, blank=True, null=True) #"Boston Water & Sewer Commission"
    contractor = models.CharField(max_length=200, blank=True, null=True) #"RJV Construction"
    permit = models.CharField(max_length=200, blank=True, null=True) #"EXCA-1363916"
    project_category = models.CharField(max_length=200, blank=True, null=True) #"NEW CONDUIT AND/OR MAIN"
    construction_notes = models.CharField(max_length=200, blank=True, null=True) #"INSTALLATION OF SEWER AND DRAIN MAINS"
    work_schedule = models.CharField(max_length=200, blank=True, null=True) #"Days & Weekends"

    expiration_date = models.DateTimeField(blank=True, null=True) #"2023-03-03 00:00:00"
    estimated_completion_date = models.DateTimeField(blank=True, null=True) #"2023-03-03 00:00:00"


    roadway_plates_in_use = models.IntegerField(blank=True, null=True) #"None" or "2"
    sidewalk_plates_in_use = models.IntegerField(blank=True, null=True) #"None" or "2"
    status = models.CharField(max_length=200, blank=True, null=True) #"STATUS"
    trench_length = models.IntegerField(blank=True, null=True) #"10"
    contact_number = models.CharField(max_length=200, blank=True, null=True) #"800-446-8946"
    number_of_works = models.IntegerField(blank=True, null=True) #"1"
    district = models.CharField(max_length=200, blank=True, null=True) # "10B"
    #location = models.PointField(default=Point()) # "initializes the location" "Point(42.32505498309912, -71.07532782322932)"
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    zip_code = models.CharField(max_length=100, blank=True, null=True)
    #location = models.PointField(default=Point()) # "initializes the location" "Point(42.32505498309912, -71.07532782322932)"

class MailingListRecord(models.Model):
    email = models.CharField(max_length=200, unique=True)
    zip_code = models.CharField(max_length=20)
    secret = models.CharField(max_length=64, blank=True) # a secret parameter, so only the user can unsubscribe themselves.
