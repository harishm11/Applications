from django.contrib import admin
from django.urls import path
from productconfigurator.views import product


urlpatterns = [

    path('product/', product.product_list, name='product_list'),
    path('product/add/', product.product_add, name='product_add'),
    path('product/edit/<int:pk>/', product.product_edit, name='product_edit'),
    path('product/delete/<int:pk>/', product.product_delete, name='product_delete'),

]
