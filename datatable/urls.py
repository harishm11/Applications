from django.urls import path
from .views import *

urlpatterns = [
    path('<str:appLabel>/<str:modelName>/',
         datatable, name='datatable'),
    path('<str:appLabel>/<str:modelName>/add/',
         addObject, name='addObject'),
    path('<str:appLabel>/<str:modelName>/edit/<int:object_id>/',
         editObject, name='editObject'),
    path('<str:appLabel>/<str:modelName>/delete/<int:object_id>/',
         deleteObject, name='deleteObject'),
    path('export/<str:appLabel>/<str:modelName>/',
         exportCsv, name='exportCsv'),
    path('import/<str:appLabel>/<str:modelName>/',
         importCsv, name='importCsv'),
    path('<str:appLabel>/<str:modelName>/clone/<int:object_id>/',
         cloneObject, name='cloneObject'),
]
