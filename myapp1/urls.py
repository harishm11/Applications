from django.contrib import admin
from django.urls import path
from myapp1 import views

urlpatterns = [
    path('myapp1', views.home,name='home'),
    path('extractpdf', views.extractpdf,name='extractpdf'),
    path('combineexcls', views.combineexcls,name='combineexcls'),

]
