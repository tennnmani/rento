from django.contrib import admin
from django.urls import path
from rooms import views
# from rooms.views import AddRoomView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.rooms, name='rooms'),
    path("addroom", views.addroom, name='addroom'),
    path("viewroom", views.viewroom, name='viewroom'),
    path("editroom/<str:pk>", views.editroom, name='editroom'),
    path("rooms", views.rooms, name='rooms'),
    path("roomdetail", views.roomdetail, name='roomdetail'),
    path("roomdetail/<str:pk>", views.roomdetail, name='roomdetail'),
    path("publicroom/<str:pk>", views.publicroom, name='publicroom'),
    path("privateroom/<str:pk>", views.privateroom, name='privateroom'),
    path("d_publicroom/<str:pk>", views.d_publicroom, name='d_publicroom'),
    path("d_privateroom/<str:pk>", views.d_privateroom, name='d_privateroom'),
    path("deleteroom/<str:pk>", views.deleteroom, name='deleteroom'),
    path('ajax/load-locations/', views.load_locations,
         name='ajax_load_locations'),  # AJAX
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)
