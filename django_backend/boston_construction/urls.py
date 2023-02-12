from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('mailing-list', views.MailingListRecordCreateView.as_view(), name="mailing-list-signup"),
    path("mailing-list/unsubscribe/<secret>", views.delete_email, name="mailing-list-unsub"),
    path("get-data", views.get_data, name="get-data")
]
