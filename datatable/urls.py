from django.urls import path
from .views import *

urlpatterns = [
    path('datatable/<str:app_label>/<str:model_name>/',
         datatable, name='datatable'),
    path('datatable/<str:app_label>/<str:model_name>/add/',
         add_object, name='add_object'),
    path('datatable/<str:app_label>/<str:model_name>/edit/<int:object_id>/',
         edit_object, name='edit_object'),
    path('datatable/<str:app_label>/<str:model_name>/delete/<int:object_id>/',
         delete_object, name='delete_object'),
    path('export/<str:app_label>/<str:model_name>/',
         export_csv, name='export_csv'),
    path('import/<str:app_label>/<str:model_name>/',
         import_csv, name='import_csv'),
]
