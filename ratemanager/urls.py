# from django.contrib import admin
from django.urls import path
from ratemanager import views


urlpatterns = [
    path('', views.rateManager,
         name='ratemanager'),
    path('openfiling/<str:data>/', views.openfiling, name="openfiling"),
    path('openexhibit/', views.openexhibit, name="openexhibit"),
    path('exhibitlist/', views.exhibitlist, name="exhibitlist"),
    path('createRB/', views.createRB, name="createRB"),
    path('uploadRB/', views.uploadRB, name="uploadRB"),
    path('loadRBtoDB/', views.loadRBtoDB, name="loadRBtoDB"),
    path('viewRB/', views.viewRB, name="viewRB"),
    path('viewRatebooksTable/', views.viewRatebooksTable, name='viewratebookstable')
]
