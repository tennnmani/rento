from django.contrib import admin
from django.urls import path
from feature import views

urlpatterns = [
    path("adminfeature", views.adminfeature, name='adminfeature'),
    path("featureroom", views.featureroom, name='featureroom'),
    path("feature_request/<str:pk>", views.feature_request, name='feature_request'),
    path("cancel_feature/<str:pk>", views.cancel_feature, name='cancel_feature'),
    path("feature_accept/<str:pk>", views.feature_accept, name='feature_accept'),
    path("decline_feature/<str:pk>", views.decline_feature, name='decline_feature'),
     path("remove_feature/<str:pk>", views.remove_feature, name='remove_feature'),
] 