from django.contrib import admin
from django.urls import path
from myapp3 import views


urlpatterns = [

	path('openfiling/<str:data>', views.openfiling, name="openfiling"),
	path('opentable', views.opentable, name="opentable"),
	path('listtables', views.listtables, name="listtables"),

	
]