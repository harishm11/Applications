from django.contrib import admin
from django.urls import path
from myapp3 import views


urlpatterns = [

	path('openfiling/<str:data>', views.openfiling, name="openfiling"),
	path('openexhibit', views.openexhibit, name="openexhibit"),
	path('exhibitlist', views.exhibitlist, name="exhibitlist"),
	path('uploadexhibit', views.uploadexhibit, name="uploadexhibit"),
	path('uploadexhibitfile', views.uploadexhibitfile, name="uploadexhibitfile"),

	
]