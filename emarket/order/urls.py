from django.urls import path
from . import views

urlpatterns = [
    path('orders', views.get_orders, name = "get_orders"),
    path('orders/<str:pk>', views.get_one_order, name = "get_orders"),
    path('orders/<str:pk>/edit', views.edit_status_order, name = "edit_status_order"),
    path('orders/<str:pk>/delete', views.delete_order, name = "delete_order"),
    path('orders/new', views.new_order, name = "new_order"),

]
