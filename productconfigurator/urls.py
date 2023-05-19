from . import views
from django.contrib import admin
from django.urls import path
from productconfigurator.views import views
from django.urls import path


urlpatterns = [
    path('', views.productconfigurator,
         name='productconfigurator'),
    path('createproduct/', views.createProduct,
         name='createproduct'),
    #     path('viewproduct/', views.viewProduct,
    #          name='viewproduct'),
    path('updateproduct/<int:product_id>/', views.updateProduct,
         name='updateproduct'),
    path('filterproduct/', views.filterProduct,
         name='filterproduct'),

]
