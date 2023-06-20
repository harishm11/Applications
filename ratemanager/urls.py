# from django.contrib import admin
from django.urls import path
from ratemanager.views import viewRB, views, createRB


urlpatterns = [
    path('', views.rateManager,
         name='ratemanager'),
    path('openfiling/<str:data>/', views.openfiling, name="openfiling"),
    path('openexhibit/', views.openexhibit, name="openexhibit"),
    path('exhibitlist/', views.exhibitlist, name="exhibitlist"),
    path('createRB/', createRB.createRB, name="createRB"),
    path('uploadRB/', createRB.uploadRB, name="uploadRB"),
    path('loadRBtoDB/', createRB.loadRBtoDB, name="loadRBtoDB"),
    path('viewRB/', viewRB.viewRB, name="viewRB"),
    path('viewExhibits/<str:rbID>/', viewRB.viewExhibits, name='viewExhibits')
]
