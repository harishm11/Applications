# from django.contrib import admin
from django.urls import path
from ratemanager.views import exportRB, viewRB, \
    views, createRB, updateRB, compareRB, \
    createTemplate, cloneRB

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
    path('viewRBbyVersionExhibits/<str:rbid>/', viewRB.viewRBbyVersionExhibits, name='viewRBbyVersionExhibits'),
    path('viewRBbyDate/', viewRB.viewRBbyDate, name="viewRBbyDate"),
    path('viewRBbyDateExhibits/<str:rbID>/', viewRB.viewRBbyDateExhibits, name='viewRBbyDateExhibits'),
    # update rb
    path('updateRB/', updateRB.updateRB, name="updateRB"),
    path('loadUpdatedRB/', updateRB.loadUpdatedRB, name="loadUpdatedRB"),
    # compare rb
    path('compareRB/', compareRB.compareRB, name="compareRB"),
    # export update RB & Empty template
    path('exportRB/', exportRB.exportRB, name="exportRB"),
    path('exportTemplate/<str:pk>/', exportRB.exportTemplate, name="exportTemplate"),
    # create rb template
    path('createTemplate/', createTemplate.createTemplate, name="createTemplate"),
    path('listExhibits/<str:pk>/', createTemplate.listExhibits, name="listExhibits"),
    path('addExhibit2Template/', createTemplate.addExhibit2Template, name="addExhibit2Template"),
    path('editExhibitTemplate/<str:pk>/', createTemplate.editExhibitTemplate, name="editExhibitTemplate"),
    path('deleteExhibitTemplate/<str:pk>/', createTemplate.deleteExhibitTemplate, name="deleteExhibitTemplate"),
    path('EditCoverages/', views.EditCoverages, name="EditCoverages"),
    # view rb template
    path('viewTemplateOptions/', viewRB.viewTemplateOptions, name="viewTemplateOptions"),
    path('viewTemplate/<str:rbID>/', viewRB.viewTemplate, name="viewTemplate"),
    # clone
    path('cloneOptions/<int:prodCode>/', cloneRB.cloneOptions, name="cloneOptions"),
    path('cloneRB/', cloneRB.cloneRB, name="cloneRB"),
]
