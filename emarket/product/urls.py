from django.urls import path
from . import views

urlpatterns = [
    #Products
    path('products/', views.get_all_products, name='get_all_products'),
    path('products/<str:pk>', views.get_one_product, name='get_one_product'),
    path('add', views.add_product, name='add_product'),
    path('update/<str:pk>', views.update_product, name='update_product'),
    path('delete/<str:pk>', views.delete_product, name='delete_product'),
    #Reviews
    path('<str:pk>/reviews', views.add_review, name='add_review'),
    path('<str:pk>/reviews/delete', views.delete_review, name='delete_review'),


]
