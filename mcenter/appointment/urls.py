from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    path("clinic/", views.ClinicAPIView.as_view()),
    path("doctor/", views.DoctorRoleChangeAPIView.as_view()),
]

routrer = DefaultRouter()
routrer.register("appointment", views.AppointmentViewSet)
urlpatterns += routrer.urls
