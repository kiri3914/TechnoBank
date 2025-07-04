from django.urls import path
from . import views


urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login_user, name='login_user'),
    path('logout', views.logout_user, name='logout_user'),
]