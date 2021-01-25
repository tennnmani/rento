from django.shortcuts import render, redirect
from .models import Enquiry
from rooms.models import Room
from user.models import User
from enquiry.forms import EnquiryForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from user.decorators import unauthenticated_user, allowed_users
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages


@login_required(login_url='user-login')
def enquirylist(request):
    # rooms = Room.objects.filter(user=request.user)
    enquirys = Enquiry.objects.filter(user=request.user)
    #pagination control
    page = request.GET.get('page', 1)

    paginator = Paginator(enquirys, 10)
    try:
        enquiry_list = paginator.page(page)
    except PageNotAnInteger:
        enquiry_list = paginator.page(1)
    except EmptyPage:
        enquiry_list = paginator.page(paginator.num_pages)
    count = enquirys.count()

    context = {
        'count' : count,
        'enquirys': enquiry_list,
        # 'rooms': rooms
    }
    return render(request, 'user/enquirylist.html', context)


def enquirycreate(request, pk):
    if request.method == 'POST':
        enquiryform = EnquiryForm(request.POST)
        if enquiryform.is_valid():
            data = Enquiry()
            user = Room.objects.get(id=pk)
            data.room = Room.objects.get(id=pk)
            data.user = User.objects.get(username=user.user)
            data.room.total_enquiry = data.room.total_enquiry +1
            data.room.user.total_enquiry = data.room.user.total_enquiry + 1
            data.name = enquiryform.cleaned_data['name']
            data.phone = enquiryform.cleaned_data['phone']
            data.email = enquiryform.cleaned_data['email']
            data.address = enquiryform.cleaned_data['address']
            data.occupation = enquiryform.cleaned_data['occupation']
            data.question = enquiryform.cleaned_data['question']
            data.save()
            data.room.save()
            data.room.user.save()
            messages.success(request, "Enquiry was sent !")
            return redirect('roomdetail', pk)
        
        return redirect('roomdetail', pk)


def roomenqiury(request, pk):
    enquirys = Enquiry.objects.get(id=pk)
    
    context = {
        'enquirys': enquirys
    }
    return render(request, 'user/roomenqiury.html', context)

def enqiurydelete(request, pk):
    enquirys = Enquiry.objects.get(id=pk)
    enquirys.delete()
    enquirys.room.save()
    enquirys.room.user.save()
    messages.info(request, "Enquiry deleted !")
    return redirect('enquirylist')