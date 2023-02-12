FROM ubuntu
COPY . .
RUN apt update && apt install -y python3-pip
RUN pip install django requests django_q tzdata
WORKDIR django_backend/
RUN ls
RUN python3 manage.py migrate
RUN python3 manage.py shell < django_q_schedule.py
RUN python3 manage.py runserver & python3 manage.py qcluster croniter
