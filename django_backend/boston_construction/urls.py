from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('mailing-list', views.MailingListRecordCreateView.as_view(), name="mailing-list-signup")
]
