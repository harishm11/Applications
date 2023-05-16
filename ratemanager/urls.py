# from django.contrib import admin
from django.urls import path
from ratemanager import views


urlpatterns = [
    path('', views.ratemanager,
         name='ratemanager'),
    path('openfiling/<str:data>/', views.openfiling, name="openfiling"),
    path('openexhibit/', views.openexhibit, name="openexhibit"),
    path('exhibitlist/', views.exhibitlist, name="exhibitlist"),
    path('uploadexhibit/', views.uploadexhibit, name="uploadexhibit"),
    path('uploadexhibitfile/', views.uploadexhibitfile, name="uploadexhibitfile"),
    path('ratebookmanager/', views.ratebookmanager, name="ratebookmanager"),
    path('filterbyfield/', views.filterbyfield, name='filterbyfield'),
    path('viewratebookstable/', views.viewratebookstable, name='viewratebookstable')
]
