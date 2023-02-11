import requests
from .models import MailingListRecord, ConstructionRecord
from django.shortcuts import render, loader
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
