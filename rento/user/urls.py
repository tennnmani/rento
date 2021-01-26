from django.contrib import admin
from django.urls import path
from user import views

urlpatterns = [ 
    path("dashboard", views.dashboard, name='dashboard'),
    path("changepassword", views.changepassword, name='changepassword'),
    path("editprofile", views.editprofile, name='editprofile'),
    path("profile", views.profile, name='profile'), 
]

