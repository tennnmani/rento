from django.shortcuts import render, HttpResponse, redirect
from user.decorators import unauthenticated_user, allowed_users
from .models import DateTracker, Rent
from user.models import User
from rooms.models import Room
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required(login_url='user-login')
@allowed_users(allowed_roles=['rento_user'])
def rent(request):
    rooms = Room.objects.filter(user=request.user)
    check_rent = Rent.objects.filter(user=request.user)

    if not check_rent:
        datetracker = DateTracker()
        datetracker.user = User.objects.get(username=request.user)
        datetracker.date_updated = datetime.now().date()
        datetracker.save()
    else:
        database_date = DateTracker.objects.get(user=request.user)
        datetracker = DateTracker.objects.get(user=request.user)
        datetracker.date_updated = datetime.now().date()
        datetracker.save()
    for room in rooms:
        print(room.pk)
        if not check_rent:
            data = Rent()
            data.user = User.objects.get(username=request.user)
            data.room_tag = room.pk
            data.amount = room.price
            data.amount_paid = 0
            data.date_paid = datetime.now().date()
            data.due = 0
            data.advance = 0
            data.rent_status = "due"
            data.save()
        else:
            date_difference = ((datetime.now().date().year - database_date.date_updated.year)
                               * 12+datetime.now().date().month-database_date.date_updated.month)
            newrent_detail = Rent.objects.filter(room_tag=room.pk)
            if not newrent_detail:
                data = Rent()
                data.user = User.objects.get(username=request.user)
                data.room_tag = room.pk
                data.amount = room.price
                data.amount_paid = 0
                data.date_paid = datetime.now().date()
                data.due = 0
                data.advance = 0
                data.rent_status = "due"
                data.save()
            if date_difference > 0:
                print(str(date_difference)+" success "+str(room.price))
            # print(datetime.now().date()- datetime(2021,1,10).date() - database_date.date_updated.year)
                rent_detail = Rent.objects.get(room_tag=room.pk)
                updated_due = rent_detail.due + date_difference*room.price - rent_detail.advance
                if updated_due < 0:
                    updated_advance = abs(updated_due)
                    updated_due = 0
                    rent_detail.rent_status = "advance"
                elif updated_due == 0:
                    updated_advance = 0
                    rent_detail.rent_status = "paid"
                else:
                    updated_advance = 0
                    rent_detail.rent_status = "due"
                print(str(updated_due)+" "+str(updated_advance))
                rent_detail.due = updated_due
                rent_detail.advance = updated_advance
                rent_detail.save()
    rents = Rent.objects.filter(user=request.user)

    #pagination control
    page = request.GET.get('page', 1)

    paginator = Paginator(rents, 10)
    try:
        rent_list = paginator.page(page)
    except PageNotAnInteger:
        rent_list = paginator.page(1)
    except EmptyPage:
        rent_list = paginator.page(paginator.num_pages)
    count = rents.count()

    context = {
        'count' : count,
        'rents': rent_list,
        'today_date': datetime.now().date(),
    }
    return render(request, 'user/rent.html', context)


def payrent(request, room_tag):
    if request.method == 'POST':
        rent = Rent.objects.get(room_tag=room_tag)
        advance = rent.advance
        due = rent.due
        amountpaid = rent.amount_paid
        advance_data = int(request.POST.get('advance'))
        due_data = int(request.POST.get('due'))
        amountpaid_data = int(request.POST.get('amountgiven'))
        if (request.POST.get('datepaid')) == str(datetime.now().date()):
            rent.date_paid = datetime.now().date()
        else:
            return redirect('rent')
        if advance_data == advance:        
            if due_data == due:
                if advance > 0:
                    rent.advance = advance + amountpaid_data
                    rent.due = 0
                    rent.rent_status = "advance"

                elif advance == 0 and ((amountpaid_data - due) < 0):
                    rent.due = due - amountpaid_data
                    rent.rent_status = "due"

                elif advance == 0 and ((amountpaid_data - due) > 0):
                    rent.advance = amountpaid_data - due
                    rent.rent_status = "advance"

                else: # advance == 0 and ((amountpaid_data - due) == 0)
                    rent.due = 0
                    rent.rent_status = "paid"
                if amountpaid > 0:
                    rent.amount_paid = amountpaid + amountpaid_data 
                else:
                    rent.amount_paid = amountpaid_data
                rent.save()
            else:
                messages.error(request, 'Please Do No Change Data')
                return redirect('rent')
        else:
            messages.error(request, 'Please Do No Change Data')
            return redirect('rent')
        
    return redirect('rent')
