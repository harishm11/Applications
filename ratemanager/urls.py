# from django.contrib import admin
from django.urls import path
from ratemanager.views import viewRB, views, createRB, updateRB


urlpatterns = [
    path('', views.rateManager,
         name='ratemanager'),
    path('openfiling/<str:data>/', views.openfiling, name="openfiling"),
    path('openexhibit/', views.openexhibit, name="openexhibit"),
    path('exhibitlist/', views.exhibitlist, name="exhibitlist"),
    # create
    path('createRB/', createRB.createRB, name="createRB"),
    path('uploadNewRB/', createRB.uploadNewRB, name="uploadNewRB"),
    path('loadNewRBtoDB/', createRB.loadNewRBtoDB, name="loadNewRBtoDB"),
    # view
    path('viewRB/', viewRB.viewRB, name="viewRB"),
    path('viewExhibits/<str:rbID>/<str:rbVer>/', viewRB.viewExhibits, name='viewExhibits'),
    # update
    path('updateRB/', updateRB.updateRB, name="updateRB"),
    path('loadUpdatedRB/', updateRB.loadUpdatedRB, name="loadUpdatedRB"),
]
