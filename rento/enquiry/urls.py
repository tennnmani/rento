from django.contrib import admin
from django.urls import path
from enquiry import views

urlpatterns = [
    path("enquirylist", views.enquirylist, name='enquirylist'),
    path("enquirycreate/<str:pk>", views.enquirycreate, name='enquirycreate'),
    path("roomenqiury/<str:pk>", views.roomenqiury, name='roomenqiury'),
    path("enqiurydelete/<str:pk>", views.enqiurydelete, name='enqiurydelete'),
]  
