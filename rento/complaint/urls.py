from django.contrib import admin
from django.urls import path
from complaint import views

urlpatterns = [
    path("admincomplaint", views.admincomplaint, name='admincomplaint'),
    path("reportcreate/<str:pk>", views.reportcreate, name='reportcreate'),
    path("reportdetail/<str:pk>", views.reportdetail, name='reportdetail'),
]