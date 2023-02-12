from django_q.models import Schedule
from time import sleep
from django_q.tasks import async_task, result

async_task("boston_construction.tasks.get_data")

async_task("boston_construction.tasks.send_email")

# Schedule.objects.create(
#     func="boston_construction.tasks.get_data",
#     minutes=1440, # once per day
#     repeats=-1,
# )

# Schedule.objects.create(
#     func="boston_construction.tasks.send_email",
#     minutes=1440, # once per day
#     repeats=-1
# )
