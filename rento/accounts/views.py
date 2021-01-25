from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from user.models import User
from user.forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from user.decorators import unauthenticated_admin,unauthenticated_user, allowed_users
from django.contrib.auth.models import Group


# Create your views here.
@unauthenticated_user
def userlogin(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, "Username or Password is incorrect")

    return render(request, 'login.html')

@login_required(login_url='user-login')
def logoutuser(request):
    logout(request)
    return redirect('user-login')

@login_required(login_url='adminlogin')
def logoutadmin(request):
    logout(request)
    return redirect('adminlogin')

@unauthenticated_user
def registration(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='rento_user')
            user.groups.add(group)

            messages.success(request, 'Account was created for ' + username)
            messages.success(request, 'Please Login.. ')
            return redirect('user-login')
    context = {
        'form': form,
    }
    return render(request, 'registration.html', context)

@unauthenticated_admin
def adminlogin(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admindashboard')
        else:
            messages.info(request, "Username or Password is incorrect")


    return render(request, 'useradmin/adminlogin.html')
