from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from .models import Employee, SubProject

from datetime import date
from datetime import timedelta


@login_required
def home(request, from_date=date.today()-timedelta(days=13), to_date=date.today()):
    employees = Employee.objects.all()
    subprojects = SubProject.objects.exclude(finished=True)
    date_span = (to_date - from_date).days + 1
    day_range = [to_date - timedelta(days=x) for x in range(0, date_span)]
    day_range.reverse()

    timesheet = []

    for subproject in subprojects:
        project_qs = subproject.timerecords.filter(date__range=(from_date, to_date), employee__in=employees).order_by('date')
        cur_date = from_date
        project_ts = []
        while cur_date <= to_date:
            date_qs = project_qs.filter(date=cur_date).order_by('employee')
            project_ts.append({
                'date': cur_date,
                'timerecords': date_qs,
                'total_hours': date_qs.aggregate(Sum('hours'))['hours__sum'] or 0,
            })
            cur_date = cur_date + timedelta(days=1)
        timesheet.append({
            'project': subproject,
            'timesheet': project_ts,
            'parent_project': subproject.parent_project,
        })

    context = {
        'employees': employees.order_by('user__username'),
        'subprojects': subprojects,
        'days': day_range,
        'timesheet': timesheet,
    }
    return render(request, 'timesheets/home.html', context)


@login_required
def employees_list(request):
    employees = Employee.objects
    context = {
        'employees': employees,
    }
    return render(request, 'timesheets/employees.html', context)


@login_required
def timesheet(request, employee=None, from_date=date.today()-timedelta(days=7), to_date=date.today()):
    if not employee:
        employees = Employee.objects.all()
    else:
        employees = Employee.objects.filter(user__username__exact=employee)
    subprojects = SubProject.objects.all()
    date_span = (to_date - from_date).days
    day_range = [to_date - timedelta(days=x) for x in range(0, date_span)]
    day_range.reverse()

    timesheet = []

    for subproject in subprojects:
        project_qs = subproject.timerecords.filter(date__range=(from_date, to_date), employee__in=employees).order_by('date')
        cur_date = from_date
        project_ts = []
        while cur_date <= to_date:
            date_qs = project_qs.filter(date=cur_date).order_by('employee')
            project_ts.append({
                'date': cur_date,
                'timerecords': date_qs,
                'total_hours': date_qs.aggregate(Sum('hours'))['hours__sum'] or 0,
            })
            cur_date = cur_date + timedelta(days=1)
        timesheet.append({
            'project': subproject,
            'timesheet': project_ts,
            'parent_project': subproject.parent_project,
        })

    context = {
        'employees': employees.order_by('user__username'),
        'subprojects': subprojects,
        'days': day_range,
        'timesheet': timesheet,
    }
    return render(request, 'timesheets/home.html', context)
