from django.shortcuts import render, HttpResponse
from rooms.models import Room
from feature.models import counter
from datetime import datetime, timedelta, date

# Create your views here.

#visitors page handler
def index(request):
    f_rooms = Room.objects.filter(featured='featured', blocked=False)
    for room in f_rooms:
        room.day_remaning = (room.feature_end - datetime.now().date()).days
        if room.day_remaning < 1:
            room.featured = 'not_featured'
            counters = counter.objects.get(id=1)
            counters.counter = counters.counter - 1
            counters.save()
            room.save()
    rooms = Room.objects.filter(featured='featured', blocked=False)
    context = {
        'rooms':rooms,
    }
    return render(request, 'index.html',context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')








