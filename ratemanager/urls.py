# from django.contrib import admin
from django.urls import path
from ratemanager import views


urlpatterns = [
    path('', views.rateManager,
         name='ratemanager'),
    path('openfiling/<str:data>/', views.openfiling, name="openfiling"),
    path('openexhibit/', views.openexhibit, name="openexhibit"),
    path('exhibitlist/', views.exhibitlist, name="exhibitlist"),
    path('createFromExcel/', views.createFromExcel, name="createFromExcel"),
    path('ratebookManager/', views.ratebookManager, name="ratebookmanager"),
    path('viewRatebooksTable/', views.viewRatebooksTable, name='viewratebookstable')
]
