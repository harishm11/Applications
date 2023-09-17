# from django.contrib import admin
from django.urls import path
from ratemanager.views import exportRB, viewRB, \
    views, createRB, updateRB, compareRB, \
    createTemplate, viewTemplate

app_name = 'ratemanager'

urlpatterns = [
    path('', views.rateManager, name='ratemanager'),
    path('openfiling/<str:data>/', views.openfiling, name="openfiling"),
    path('openexhibit/', views.openexhibit, name="openexhibit"),
    path('exhibitlist/', views.exhibitlist, name="exhibitlist"),
    # create rb
    path('createRB/', createRB.createRB, name="createRB"),
    path('uploadNewRB/', createRB.uploadNewRB, name="uploadNewRB"),
    path('loadNewRBtoDB/', createRB.loadNewRBtoDB, name="loadNewRBtoDB"),
    # view rb
    path('viewRB/', viewRB.viewRB, name="viewRB"),
    path('viewRBbyVersion/', viewRB.viewRBbyVersion, name="viewRBbyVersion"),
    path('viewRBbyVersionExhibits/<str:rbID>/<str:rbVer>/', viewRB.viewRBbyVersionExhibits, name='viewRBbyVersionExhibits'),
    path('viewRBbyDate/', viewRB.viewRBbyDate, name="viewRBbyDate"),
    path('viewRBbyDateExhibits/<str:rbID>/', viewRB.viewRBbyDateExhibits, name='viewRBbyDateExhibits'),
    # update rb
    path('updateRB/', updateRB.updateRB, name="updateRB"),
    path('loadUpdatedRB/', updateRB.loadUpdatedRB, name="loadUpdatedRB"),
    # compare rb
    path('compareRB/', compareRB.compareRB, name="compareRB"),
    # export update RB & Empty template
    path('exportRB/', exportRB.exportRB, name="exportRB"),
    path('exportTemplate/<int:pk>/', exportRB.exportTemplate, name="exportTemplate"),
    # create rb template
    path('createTemplate/', createTemplate.createTemplate, name="createTemplate"),
    path('createExhibitsAndVariables/<int:pk>/', createTemplate.createExhibitsAndVariables.as_view(), name="createExhibitsAndVariables"),
    # view rb template
    path('viewTemplate/', viewTemplate.viewTemplate, name="viewTemplate")
]
