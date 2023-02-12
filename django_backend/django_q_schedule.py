from django_q.models import Schedule
Schedule.objects.create(
    func="boston_construction.tasks.get_data",
    minutes=1,
    repeats=-1,
)
