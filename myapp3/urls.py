from django.contrib import admin
from django.urls import path
from myapp3 import views


urlpatterns = [
	path('myapp3', views.home, name="home"),

	
]