from django.contrib import admin
from django.urls import path
from useradmin import views


urlpatterns = [
    path("admindashboard", views.admindashboard, name='admindashboard'),
    path("adminchangepassword", views.adminchangepassword, name='adminchangepassword'),
    path("adminroomlist", views.adminroomlist, name='adminroomlist'),
    path("block_user/<str:pk>", views.block_user, name='block_user'),
    path("unblock_user/<str:pk>", views.unblock_user, name='unblock_user'),
    path("delete_user/<str:pk>", views.delete_user, name='delete_user'),
    path("admin_delete_room/<str:pk>", views.admin_delete_room, name='admin_delete_room'),
    path("admin_delete_c_room/<str:pk>", views.admin_delete_c_room, name='admin_delete_c_room'),
    path("c_discard/<str:pk>", views.c_discard, name='c_discard'),
    path("blockroom/<str:pk>", views.blockroom, name='blockroom'),
    path("unblockroom/<str:pk>", views.unblockroom, name='unblockroom'),
    path("c_blockroom/<str:pk>", views.c_blockroom, name='c_blockroom'),
    path("d_adminroomlist/<str:pk>", views.d_adminroomlist, name='d_adminroomlist'),
]