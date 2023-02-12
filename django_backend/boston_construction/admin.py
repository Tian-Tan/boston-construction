from django.contrib import admin
from .models import MailingListRecord, Rule

# Register your models here.
admin.site.register(MailingListRecord)
admin.site.register(Rule)
