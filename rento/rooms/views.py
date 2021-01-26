from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import TemplateView
from .forms import AddRoomForm, EditForm
from enquiry.forms import EnquiryForm
from complaint.forms import reportForm
from .models import City, Location, Room
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from user.decorators import unauthenticated_user, allowed_users
from user.models import User
from user.forms import CreateUserForm
from feature.models import counter
from django.contrib import messages

# Create your views here.

# class AddRoomView(TemplateView):
#     template_name = 'user/addroom.html'

#     def get(self, request):
#         form = AddRoomForm()
#         args = {
#             'form': form
#             }
#         return render(request, self.template_name, args)
    
#     def post(self, request):
#         form = AddRoomForm(request.POST, request.FILES)
#         if form.is_valid():
#             room = form.save(commit=False)
#             room.save()
#             form = AddRoomForm()
#             return redirect('dashboard')
#         args = {
#             'form' : form
#         }
#         return render(request, self.template_name, args)

@allowed_users(allowed_roles=['rento_user'])
def addroom(request):
    addroomform = AddRoomForm()
    if request.method == 'POST':
        addroomform = AddRoomForm(request.POST, request.FILES)
        if addroomform.is_valid():
            data = Room()
            data.user = request.user

            data.city = addroomform.cleaned_data['city']
            data.location = addroomform.cleaned_data['location']
            data.house_number = addroomform.cleaned_data['house_number']
            data.floor = addroomform.cleaned_data['floor']
            data.price = addroomform.cleaned_data['price']
            data.image1 = addroomform.cleaned_data['image1']
            data.image2 = addroomform.cleaned_data['image2']
            data.image3 = addroomform.cleaned_data['image3']
            data.water = addroomform.cleaned_data['water']
            data.internet = addroomform.cleaned_data['internet']
            data.parking = addroomform.cleaned_data['parking']
            data.description = addroomform.cleaned_data['description']
            data.user.total_rooms = data.user.total_rooms +1
            data.user.save()
            data.save()
            return redirect('dashboard')
    args = {
        'addroomform': addroomform
    }
    return render(request, 'user/addroom.html', args)

# AJAX
@login_required(login_url='user-login')
def load_locations(request):
    city_id = request.GET.get('city_id')
    if city_id == '':
        locations = ""
    else:
        locations = Location.objects.filter(city_id=city_id).all()
    return render(request, 'user/location_dropdown_list_options.html', {'locations': locations})
    # return JsonResponse(list(cities.values('id', 'name')), safe=False)

@allowed_users(allowed_roles=['rento_user'])
def viewroom(request):
    rooms = Room.objects.filter(user= request.user)
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
    }
    return render(request, 'user/viewroom.html',context)

@allowed_users(allowed_roles=['rento_user'])
def editroom(request, pk):
    rooms = Room.objects.get(id=pk)
    form = EditForm(instance=rooms)
    context = {
        'form': form,
        'room': rooms
    }
    if request.method == 'POST':
            form = EditForm(request.POST, instance=rooms)
            if form.is_valid():
                if form.cleaned_data['room_status'] == 'private':
                    if rooms.featured == 'featured':
                        rooms.featured = 'not_featured'
                        counters = counter.objects.get(id=1)
                        counters.counter = counters.counter - 1
                        counters.save()
                form.save()
                return redirect('viewroom')
    return render(request, 'user/editroom.html',context)

def rooms(request):
    room_list = Room.objects.filter(room_status= 'public', blocked= False ).order_by('-date_posted')
    locations = Location.get_all_locations()
    locationID = request.GET.get('location')
    facility1 = request.GET.get('water')
    facility2 = request.GET.get('internet')
    facility3 = request.GET.get('parking')
    pricefilter = request.GET.get('pricefilter')
    if not facility1:
        facility1=False
    if not facility2:
        facility2=False
    if not facility3:
        facility3=False
    values = {
            'locationID': locationID,
            'facility1': facility1,
            'facility2': facility2,
            'facility3': facility3,
            'pricefilter': pricefilter,
        }

    #location filter
    if locationID:
        room_list = Room.get_all_rooms_by_filter(locationID).order_by('-date_posted')

    #facility filter
    if facility1 or facility2 or facility3:
        room_list = Room.get_all_rooms_by_waterinternetparkingfilter(facility1,facility2,facility3).order_by('-date_posted')
    
    if locationID and (facility1 or facility2 or facility3):
        room_list = Room.get_all_rooms_by_allfilter(locationID,facility1,facility2,facility3).order_by('-date_posted')
    
    #price filter
    if pricefilter == "1":
        room_list = Room.objects.filter().order_by('price')

    if (pricefilter == "2"):
        room_list = Room.objects.filter().order_by('-price')

    if (pricefilter == "1") and locationID:
        room_list = Room.get_all_rooms_by_filter(locationID).order_by('price')

    if (pricefilter == "2")  and locationID:
        room_list = Room.get_all_rooms_by_filter(locationID).order_by('-price')

    if (pricefilter == "1") and (facility1 or facility2 or facility3):
        room_list = Room.get_all_rooms_by_waterinternetparkingfilter(facility1,facility2,facility3).order_by('price')

    if (pricefilter == "2")  and (facility1 or facility2 or facility3):
        room_list = Room.get_all_rooms_by_waterinternetparkingfilter(facility1,facility2,facility3).order_by('-price')

    if (pricefilter == "1") and locationID and (facility1 or facility2 or facility3):
        room_list = Room.get_all_rooms_by_allfilter(locationID,facility1,facility2,facility3).order_by('price')

    if (pricefilter == "2")  and locationID and (facility1 or facility2 or facility3):
        room_list = Room.get_all_rooms_by_allfilter(locationID,facility1,facility2,facility3).order_by('-price')
        
    #pagination control
    page = request.GET.get('page', 1)

    paginator = Paginator(room_list, 8)
    try:
        rooms = paginator.page(page)
    except PageNotAnInteger:
        rooms = paginator.page(1)
    except EmptyPage:
        rooms = paginator.page(paginator.num_pages)
    
    data = {}
    data['rooms'] = rooms
    data['locations'] = locations
    data['values'] = values
    return render(request, 'rooms.html', data)

def roomdetail(request, pk):
    rooms = Room.objects.get(id=pk)
    enquiryform = EnquiryForm()
    reportform = reportForm()
    if rooms.user != request.user:
        rooms.views = rooms.views + 1
        rooms.user.total_views = rooms.user.total_views + 1
        rooms.user.save()
        rooms.save()
    if rooms.location:
        print(rooms.location)
        room_list = Room.get_all_rooms_by_filter(rooms.location).exclude(id=pk)
    return render(request, 'roomdetail.html', {'rooms': rooms, 'enquiryform':enquiryform, 'reportform':reportform,  'similarroom': room_list})

@login_required(login_url='user-login')
def deleteroom(request, pk):
    rooms = Room.objects.get(id=pk)
    rooms.user.total_rooms = rooms.user.total_rooms -1
    if rooms.user.total_rooms < 0:
        rooms.user.total_rooms = 0
    rooms.user.total_views = rooms.user.total_views - rooms.views
    rooms.user.total_enquiry = rooms.user.total_enquiry - rooms.total_enquiry
    if rooms.featured == 'featured':
        counters = counter.objects.get(id=1)
        counters.counter = counters.counter - 1
        counters.save()
    messages.success(request, ('Room no {} was deleted ').format(rooms.id))
    rooms.delete()
    rooms.user.save()
    
    return redirect('viewroom')


def privateroom(request, pk):
    rooms = Room.objects.get(id = pk)
    rooms.room_status = 'private'
    rooms.save()
    return redirect('viewroom')

def publicroom(request, pk):
    rooms = Room.objects.get(id = pk)
    rooms.room_status = 'public'
    rooms.save()
    return redirect('viewroom')


def d_privateroom(request, pk):
    rooms = Room.objects.get(id = pk)
    rooms.room_status = 'private'
    rooms.save()
    return redirect('dashboard')

def d_publicroom(request, pk):
    rooms = Room.objects.get(id = pk)
    rooms.room_status = 'public'
    rooms.save()
    return redirect('dashboard')