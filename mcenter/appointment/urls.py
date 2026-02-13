from django.urls import path
from rest_framework.routers import BaseRouter

from . import views

urlpatterns = [
    path("clinick/", views.ClinickAPIView().as_view()),
    path("doctor/", views.DoctorAPIView().as_view()),
]
