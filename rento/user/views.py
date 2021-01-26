from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users
from rooms.models import Room
from enquiry.models import Enquiry
from .models import User
from .forms import EditUserForm, ChangePasswordForm
from django.views.generic import TemplateView
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger







@login_required(login_url='user-login')
@allowed_users(allowed_roles=['rento_user'])
def dashboard(request):
    rooms = Room.objects.filter(user=request.user)

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
    # count = enquirys.count()
    context = {
        'count' : count,
        'rooms': room_list
    }
    return render(request, 'user/dashboard.html', context)


@login_required(login_url='user-login')
@allowed_users(allowed_roles=['rento_user'])
def profile(request):

    users = User.objects.filter(username=request.user)
    context = {
        'users': users
    }
    return render(request, 'user/profile.html', context)


@login_required(login_url='user-login')
@allowed_users(allowed_roles=['rento_user'])
def editprofile(request):
    users = User.objects.get(username=request.user)
    form = EditUserForm(instance=users)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=users)
        if form.is_valid():
            form.save()
            return redirect('profile')
    context = {
        'form': form,
        'users': users
    }
    return render(request, 'user/editprofile.html', context)


@login_required(login_url='user-login')
@allowed_users(allowed_roles=['rento_user'])
def changepassword(request):
    if request.method == 'POST':
        form = ChangePasswordForm(data=request.POST, user=request.user)

        if form.data['new_password1'] !=  form.data['new_password2']:
            messages.error(request, 'New Passwords doesn\'t match')
            return redirect('changepassword')
        elif form.is_valid():
            if form.cleaned_data['old_password'] != form.cleaned_data['new_password1']:
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, 'Password changed sucesfully !!')
                return redirect('dashboard')
            else:
                messages.error(request, 'New passwords must be different than old one ')
                return redirect('changepassword')
        else:
            messages.error(request, 'Please enter correct old passwords')
            return redirect('changepassword')
    else:
        form = ChangePasswordForm(user=request.user)

        args = {'form': form}
        return render(request, 'user/changepassword.html', args)



    # users = User.objects.get(username=request.user)
    # form = ChangePasswordForm()
    # if request.method == 'POST':
    #     form = ChangePasswordForm(request.POST)   
    #     if form.is_valid():
    #         u = User.objects.get(username=request.user)
    #         password = form.cleaned_data['password1']
    #         u.set_password(password)
    #         form.save()
    #         return redirect('profile')
    # context = {
    #     'form': form,
    #     'users': users
    # }

    # return render(request, 'user/changepassword.html',context)
