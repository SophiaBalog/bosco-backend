from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list_view, name='product_list'),
    path('add/', views.product_add_view, name='add_product'),
    path('edit/<int:pk>/', views.product_edit_view, name='product_edit'),
    path('delete/<int:pk>/', views.product_delete_view, name='product_delete'),
]