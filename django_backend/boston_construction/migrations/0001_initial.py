# Generated by Django 4.1.6 on 2023-02-11 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ConstructionRecord",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("_id", models.IntegerField()),
                ("neighborhood", models.CharField(max_length=100)),
                ("street", models.CharField(max_length=100)),
                ("address_1", models.IntegerField()),
                ("address_2", models.IntegerField()),
                ("intersection", models.CharField(max_length=100)),
                ("start", models.CharField(max_length=100)),
                ("to", models.CharField(max_length=100)),
                ("permittee", models.CharField(max_length=200)),
                ("contractor", models.CharField(max_length=200)),
                ("permit", models.CharField(max_length=200)),
                ("project_category", models.CharField(max_length=200)),
                ("construction_notes", models.CharField(max_length=200)),
                ("work_schedule", models.CharField(max_length=200)),
                ("expiration_date", models.CharField(max_length=200)),
                ("estimated_completion_date", models.CharField(max_length=200)),
                ("roadway_plates_in_use", models.IntegerField()),
                ("sidewalk_plates_in_use", models.IntegerField()),
                ("status", models.CharField(max_length=200)),
                ("trench_length", models.IntegerField()),
                ("contact_number", models.CharField(max_length=200)),
                ("number_of_works", models.IntegerField()),
                ("district", models.CharField(max_length=200)),
                ("latitude", models.FloatField()),
                ("longitude", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="MailingListRecord",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("email", models.CharField(max_length=200)),
                ("zip_code", models.CharField(max_length=20)),
                ("secret", models.CharField(max_length=64)),
            ],
        ),
    ]
