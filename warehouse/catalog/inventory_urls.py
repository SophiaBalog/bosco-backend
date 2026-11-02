from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_list_view, name='inventory_list'),
    path('alerts/', views.inventory_alerts_view, name='inventory_alerts'),
    path('replenish/<int:count>/', views.inventory_replenish_view, name='inventory_replenish'),
    path('replenish/<int:count>', views.inventory_replenish_view),
]