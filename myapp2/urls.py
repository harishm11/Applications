from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from myapp2.views.driver import *
from myapp2.views.incident import *
from myapp2.views.vehicle import *


urlpatterns = [
    path('driver-list/', driverList, name="driver-list"),
	path('driver-detail/<str:pk>/', driverDetail, name="driver-detail"),
	path('driver-create/', driverCreate, name="driver-create"),

	path('driver-update/<str:pk>/', driverUpdate, name="driver-update"),
	path('driver-delete/<str:pk>/', driverDelete, name="driver-delete"),

    path('vehicle-list/', vehicleList, name="vehicle-list"),
	path('vehicle-detail/<str:pk>/', vehicleDetail, name="vehicle-detail"),
	path('vehicle-create/', vehicleCreate, name="vehicle-create"),

	path('vehicle-update/<str:pk>/', vehicleUpdate, name="vehicle-update"),
	path('vehicle-delete/<str:pk>/', vehicleDelete, name="vehicle-delete"),
    
    path('incident-list/', incidentList, name="incident-list"),
	path('incident-detail/<str:pk>/', incidentDetail, name="incident-detail"),
	path('incident-create/', incidentCreate, name="incident-create"),

	path('incident-update/<str:pk>/', incidentUpdate, name="incident-update"),
	path('incident-delete/<str:pk>/', incidentDelete, name="incident-delete"),
]



