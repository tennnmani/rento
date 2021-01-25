from django.shortcuts import render, HttpResponse, redirect
from user.decorators import unauthenticated_user, allowed_users
from rooms.models import Room
from user.models import User
from feature.models import counter
from complaint.models import report
from django.http import HttpResponseRedirect
from complaint.models import report
from user.views import ChangePasswordForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@allowed_users(allowed_roles=['rento_admin'])
def admindashboard(request):

    # rooms = Room.objects.all()
    users = User.objects.filter(groups="2")

        #pagination control
    page = request.GET.get('page', 1)

    paginator = Paginator(users, 10)
    try:
        user_list = paginator.page(page)
    except PageNotAnInteger:
        user_list = paginator.page(1)
    except EmptyPage:
        user_list = paginator.page(paginator.num_pages)
    count = users.count()
    content = {
        'count': count,
        'users': user_list,
        # 'rooms': rooms,
    }

    return render(request, 'useradmin/admindashboard.html', content)


@allowed_users(allowed_roles=['rento_admin'])
def adminchangepassword(request):
    if request.method == 'POST':
        form = ChangePasswordForm(data=request.POST, user=request.user)

        if form.data['new_password1'] !=  form.data['new_password2']:
            messages.error(request, 'New Passwords doesn\'t match')
            return redirect('adminchangepassword')
        elif form.is_valid():
            if form.cleaned_data['old_password'] != form.cleaned_data['new_password1']:
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, 'Password changed sucesfully !!')
                return redirect('admindashboard')
            else:
                messages.error(request, 'New passwords must be different than old one ')
                return redirect('adminchangepassword')
        else:
            messages.error(request, 'Please enter correct old passwords')
            return redirect('adminchangepassword')
    else:
        form = ChangePasswordForm(user=request.user)

        args = {'form': form}
        return render(request, 'useradmin/adminchangepassword.html', args)
    return render(request, 'useradmin/adminchangepassword.html')


@allowed_users(allowed_roles=['rento_admin'])
def adminroomlist(request):
    rooms = Room.objects.all()
    
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
        'count':count,
        'rooms': room_list
    }

    return render(request, 'useradmin/adminroomlist.html', context)


def block_user(request, pk):
    users = User.objects.get(id=pk)
    users.user_status = 'blocked'
    users.save()
    rooms = Room.objects.filter(user=pk)
    for room in rooms:
        room.blocked = True
        room.save()
        if room.featured == 'featured':
            room.featured = 'not_featured'
            room.save()
            counters = counter.objects.get(id=1)
            counters.counter = counters.counter - 1
            counters.save()
        else:
            room.featured = 'not_featured'
            room.save()
        
    return redirect('admindashboard')

def unblock_user(request, pk):
    users = User.objects.get(id=pk)
    users.user_status = 'clear'
    users.save()
    rooms = Room.objects.filter(user=pk)
    for room in rooms:
        room.blocked = False
        room.save()
    return redirect('admindashboard')

def delete_user(request, pk):
    users = User.objects.get(id=pk)
    messages.info(request, ('User : id {} was deleted ').format(users.id))
    users.delete()
    # rooms = Room.objects.filter(user=pk)
    # for room in rooms:
    #     room.blocked = False
    #     room.save()
    return redirect('admindashboard')


def admin_delete_room(request, pk):
    rooms = Room.objects.get(id=pk)
    print(rooms.user.total_rooms)
    rooms.user.total_views = rooms.user.total_views - rooms.views 
    rooms.user.total_enquiry = rooms.user.total_enquiry - rooms.total_enquiry
    rooms.user.total_rooms = rooms.user.total_rooms - 1  
    if rooms.user.total_rooms < 0:
        rooms.user.total_rooms = 0
    rooms.user.save()    
    if rooms.featured == 'featured':
        counters = counter.objects.get(id=1)
        counters.counter = counters.counter - 1
        counters.save()
    messages.info(request, ('Room no {} was deleted ').format(rooms.id))
    rooms.delete()
    return redirect('adminroomlist')

def admin_delete_c_room(request, pk):
    rooms = Room.objects.get(id=pk)
    rooms.user.total_views = rooms.user.total_views - rooms.views 
    rooms.user.total_enquiry = rooms.user.total_enquiry - rooms.total_enquiry
    rooms.user.total_rooms = rooms.user.total_rooms - 1  
    if rooms.user.total_rooms < 0:
        rooms.user.total_rooms = 0
    rooms.user.save() 
    if rooms.featured == 'featured':
        counters = counter.objects.get(id=1)
        counters.counter = counters.counter - 1
        counters.save()
    messages.info(request, ('Room no {} was deleted ').format(rooms.id))
    rooms.delete()
    return redirect('admincomplaint')

def c_discard(request, pk):
    reports = report.objects.get(id=pk)
    if reports.room.blocked == False:
        reports.room.total_report = reports.room.total_report -1 
        reports.room.user.total_reports = reports.room.user.total_reports - 1
        reports.room.save()
        reports.room.user.save()
    messages.success(request, ('report no {} was discarded ').format(reports.id))
    reports.delete()
    return redirect('admincomplaint')


def blockroom(request, pk):
    rooms = Room.objects.get(id=pk)
    rooms.blocked = True
    rooms.save()
    if rooms.featured == 'featured':
        rooms.featured = 'not_featured'
        rooms.save()
        counters = counter.objects.get(id=1)
        counters.counter = counters.counter - 1
        counters.save()
    else:
        rooms.featured = 'not_featured'
        rooms.save()
    messages.info(request, ('Room no {} was blocked ').format(rooms.id))
    return redirect('adminroomlist')

def unblockroom(request, pk):
    rooms = Room.objects.get(id=pk)
    rooms.blocked = False
    messages.success(request, ('Room no {} was unblocked ').format(rooms.id))
    rooms.save()
    return redirect('adminroomlist')

def c_blockroom(request, pk):
    reports = report.objects.get(id=pk)
    reports.room.blocked = True
    reports.room.save()
    if reports.room.featured == 'featured':
        reports.room.featured = 'not_featured'
        reports.room.save()
        counters = counter.objects.get(id=1)
        counters.counter = counters.counter - 1
        counters.save()
    else:
        reports.room.featured = 'not_featured'
        reports.room.save()
    reports.delete()
    messages.info(request, ('room no {} was blocked ').format(reports.room.id))
    return redirect('admincomplaint')


@allowed_users(allowed_roles=['rento_admin'])
def d_adminroomlist(request,pk):
    rooms = Room.objects.filter(user=pk)
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
        'count':count,
        'rooms': room_list
    }

    return render(request, 'useradmin/adminroomlist.html', context)
