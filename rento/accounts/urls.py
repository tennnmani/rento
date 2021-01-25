from django.contrib import admin
from django.urls import path
from accounts import views

urlpatterns = [
    path("", views.userlogin, name='user-login'),
    path("userlogin", views.userlogin, name='user-login'),
    path("adminlogin", views.adminlogin, name='adminlogin'),
    path("logoutuser", views.logoutuser, name='logoutuser'),
    path("registration", views.registration, name='registration'),
    path("logoutadmin", views.logoutadmin, name='logoutadmin'),
]    