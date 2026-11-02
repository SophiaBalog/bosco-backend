from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list_view, name='product_list'),
    path('add/', views.product_add_view, name='add_product'),
    path('edit/<int:pk>/', views.product_edit_view, name='product_edit'),
    path('delete/<int:pk>/', views.product_delete_view, name='product_delete'),
    path('manage/', views.ProductManageListView.as_view(), name='manage_list'),
    path('manage/add/', views.ProductCreateView.as_view(), name='manage_add'),
    path('manage/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='manage_edit'),
    path('manage/<int:pk>/publish/', views.product_publish_view, name='manage_publish'),
    path('stats/', views.ProductStatsView.as_view(), name='stats'),
]