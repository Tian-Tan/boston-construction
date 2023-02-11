from django.contrib.gis.db import models, Point


# Create your models here.
class ConstructionRecord(models.Model):
    """
    Model for construction data, as pulled directly from data.boston.gov
    https://data.boston.gov/dataset/public-works-active-work-zones/resource/36fcf981-e414-4891-93ea-f5905cec46fc
    """
    _id = models.IntegerField() # "1"
    neighborhood = models.CharField(max_length=100) # "ROXBURY"
    street = models.CharField(max_length=100) # "FALCON ST"
    address_1 = models.IntegerField() # "3"
    address_2 = models.IntegerField() # "4"
    intersection = models.CharField(max_length=100) # "BOYLSTON ST"
    start = models.CharField(max_length=100) # "DUDLEY ST"
    to = models.CharField(max_length=100) #"WINTHROP ST"
    permittee = models.CharField(max_length=200) #"Boston Water & Sewer Commission"
    contractor = models.CharField(max_length=200) #"RJV Construction"
    permit = models.CharField(max_length=200) #"EXCA-1363916"
    project_category = models.CharField(max_length=200) #"NEW CONDUIT AND/OR MAIN"
    construction_notes = models.CharField(max_length=200) #"INSTALLATION OF SEWER AND DRAIN MAINS"
    work_schedule = models.CharField(max_length=200) #"Days & Weekends"
    expiration_date = models.CharField(max_length=200) #"2023-03-03 00:00:00"
    estimated_completion_date = models.CharField(max_length=200) #"2023-03-03 00:00:00"
    roadway_plates_in_use = models.IntegerField() #"None" or "2"
    sidewalk_plates_in_use = models.IntegerField() #"None" or "2"
    status = models.CharField(max_length=200) #"STATUS"
    trench_length = models.IntegerField() #"10"
    contact_number = models.CharField(max_length=200) #"800-446-8946"
    number_of_works = models.IntegerField() #"1"
    district = models.CharField(max_length=200) # "10B"
    location = models.PointField(default=Point()) # "initializes the location" "Point(42.32505498309912, -71.07532782322932)"