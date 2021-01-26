from .models import report
from rooms.models import Room
from complaint.forms import reportForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect
from user.decorators import unauthenticated_user, allowed_users
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@allowed_users(allowed_roles=['rento_admin'])
def admincomplaint(request):
    reports = report.objects.all()
    #pagination control
    page = request.GET.get('page', 1)

    paginator = Paginator(reports, 10)
    try:
        report_list = paginator.page(page)
    except PageNotAnInteger:
        report_list = paginator.page(1)
    except EmptyPage:
        report_list = paginator.page(paginator.num_pages)
    count = reports.count()
    context = {
        'count':count,
        'reports': report_list,
    }
    return render(request, 'useradmin/admincomplaint.html',context)


def reportcreate(request, pk):
    if request.method == 'POST':
        reportform = reportForm(request.POST)
        if reportform.is_valid():
            data = report()

            data.room = Room.objects.get(id=pk)
            data.room.user.total_reports = data.room.user.total_reports + 1
            data.room.total_report = data.room.total_report + 1
            data.report_type = reportform.cleaned_data['report_type']
            data.report_description = reportform.cleaned_data['report_description']
            data.save()
            data.room.save()
            data.room.user.save()
            return redirect('roomdetail', pk)
        return redirect('roomdetail', pk)

def reportdetail(request, pk):
    reports = report.objects.get(id=pk)
    
    context = {
        'reports': reports
    }
    return render(request, 'useradmin/reportdetail.html', context)