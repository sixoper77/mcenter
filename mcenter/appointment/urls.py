from django.urls import path

from . import views

urlpatterns = [
    path("clinic/", views.ClinicAPIView().as_view()),
    path("doctor/", views.DoctorAPIView().as_view()),
]
