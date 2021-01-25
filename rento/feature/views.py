from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from user.decorators import unauthenticated_user, allowed_users
from rooms.models import Room
from datetime import datetime, timedelta, date
from .models import counter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
@allowed_users(allowed_roles=['rento_user'])
def featureroom(request):
    rooms = Room.objects.filter(user= request.user)
    f_rooms = Room.objects.filter(user= request.user, featured='featured')
    
    for room in rooms:
        if room.featured == 'denied':
            room.day_remaning = (room.declined_date - datetime.now().date()).days
            if room.day_remaning < 1:
                room.featured = 'not_featured'
                room.save()
            room.save()
        if room.featured == 'featured':
            room.day_remaning = (room.feature_end - datetime.now().date()).days
            if room.day_remaning < 1:
                room.featured = 'not_featured'
                counters = counter.objects.get(id=1)
                counters.counter = counters.counter - 1
                counters.save()
                room.save()
            room.save()
             
    #pagination control
    page = request.GET.get('page', 1)

    paginator = Paginator(rooms, 10)
    try:
        room_list = paginator.page(page)
    except PageNotAnInteger:
        room_list = paginator.page(1)
    except EmptyPage:
        room_list = paginator.page(paginator.num_pages)
    count = rooms.count()

    context = {
        'count' : count,
        'rooms': room_list,
        'f_rooms' : f_rooms,
    }
    return render(request, 'user/featureroom.html',context)

@allowed_users(allowed_roles=['rento_admin'])
def adminfeature(request):
    room_list = Room.objects.filter(featured= 'feature_request', blocked=False)
    f_rooms = Room.objects.filter(featured= 'featured', blocked=False)
    counters = counter.objects.get(id=1)
    for room in f_rooms:
        room.day_remaning = (room.feature_end - datetime.now().date()).days
        if room.day_remaning < 1:
            return redirect('remove_feature',room.id)
        room.save()
    
      #pagination control
    page = request.GET.get('page', 1)

    paginator = Paginator(room_list, 8)
    try:
        rooms = paginator.page(page)
    except PageNotAnInteger:
        rooms = paginator.page(1)
    except EmptyPage:
        rooms = paginator.page(paginator.num_pages)
    
    count = room_list.count()
    # count = enquirys.count()
    context = {
        'count' : count,
        'rooms': rooms,
        'f_rooms':f_rooms,
        'counters' : counters
       
    }
    return render(request, 'useradmin/adminfeature.html',context)

def feature_request(request, pk):
    rooms = Room.objects.get(id=pk)
    rooms.featured = 'feature_request'
    rooms.save()
    return redirect('featureroom')

def cancel_feature(request, pk):
    rooms = Room.objects.get(id=pk)
    rooms.featured = 'not_featured'
    rooms.save()
    return redirect('featureroom')

def remove_feature(request, pk):
    rooms = Room.objects.get(id=pk)
    rooms.featured = 'not_featured'
    counters = counter.objects.get(id=1)
    counters.counter = counters.counter - 1
    counters.save()
    rooms.save()
    return redirect('adminfeature')

def feature_accept(request, pk):
    rooms = Room.objects.get(id=pk)
    counters = counter.objects.get(id=1)
    counters.counter = counters.counter + 1
    counters.save()
    rooms.featured = 'featured'
    rooms.times_featured = rooms.times_featured +1
    rooms.featured_date = datetime.now().date()
    rooms.feature_end = rooms.featured_date + timedelta(days=10)
    rooms.save()
    return redirect('adminfeature')

    
def decline_feature(request, pk):
    rooms = Room.objects.get(id=pk)
    rooms.featured = 'denied'
    rooms.declined_date = datetime.now().date() +  timedelta(days=3)
    rooms.save()
    return redirect('adminfeature')