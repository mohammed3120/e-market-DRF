from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('user/info', views.current_user, name='user_info'),
    path('user/update', views.update_user, name='update_user'),
    path('user/forgot_password', views.forgot_password, name='forgot_password'),
    path('user/reset_password/<str:token>', views.reset_password, name='reset_password'),
]
