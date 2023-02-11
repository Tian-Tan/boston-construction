from django.shortcuts import render, loader
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from boston_construction.models import MailingListRecord


def index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))

class MailingListRecordCreateView(CreateView):
    model = MailingListRecord
    fields = ["email", "zip_code"]
