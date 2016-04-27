from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
import json
from django.db.models import Sum
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.views.generic import ListView

from .models import TimeRecord, Employee, SubProject, Project
from .forms import TimeRecordForm, SubProjectForm, ProjectForm

from datetime import date
from datetime import timedelta


def get_timesheet(**kwargs):
    if 'employee' in kwargs:
        employees = Employee.objects.filter(user__username__exact=kwargs['employee'])
    else:
        employees = Employee.objects.all().order_by('user__username')

    to_date = kwargs.get('to_date', date.today())
    from_date = kwargs.get('from_date', date.today() - timedelta(days=7))

    subprojects = SubProject.objects.all()
    date_span = (to_date - from_date).days
    day_range = [to_date - timedelta(days=x) for x in range(0, date_span + 1)]
    day_range.reverse()

    timesheet = []

    for subproject in subprojects:
        subproject_qs = subproject.timerecords.filter(date__range=(from_date, to_date), employee__in=employees).order_by('date')
        cur_date = from_date
        subproject_ts = []
        while cur_date <= to_date:
            date_qs = subproject_qs.filter(date=cur_date).order_by('employee')
            subproject_ts.append({
                'date': cur_date,
                'timerecords': date_qs,
                'total_hours': date_qs.aggregate(Sum('hours'))['hours__sum'] or 0,
            })
            cur_date = cur_date + timedelta(days=1)
        timesheet.append({
            'subproject': subproject,
            'timesheet': subproject_ts,
            'project': subproject.parent_project,
        })

    cur_date = from_date
    totalhours_ts = []
    while cur_date <= to_date:
        hours_by_day = []
        for employee in employees:
            timerecord_qs = TimeRecord.objects.filter(date=cur_date, employee=employee)
            totalhours_by_day = timerecord_qs.aggregate(Sum('hours'))['hours__sum'] or None
            if totalhours_by_day != 0:
                hours_by_day.append({
                    'employee': employee,
                    'total_hours': totalhours_by_day,
                })

        totalhours_ts.append(hours_by_day)

        cur_date = cur_date + timedelta(days=1)

    timesheet.append({
        'subproject': subproject,
        'timesheet': subproject_ts,
        'project': subproject.parent_project,
    })

    context = {
        'employees': employees.order_by('user__username'),
        'subprojects': subprojects,
        'days': day_range,
        'timesheet': timesheet,
        'total_hours': totalhours_ts,
        'total': TimeRecord.objects.filter(date__range=(from_date, to_date)).aggregate(Sum('hours'))['hours__sum'] or 0,
        'start_date': from_date,
        'end_date': to_date,
    }

    return context


@login_required
def home(request, from_date=date.today()-timedelta(days=7), to_date=date.today()):
    context = get_timesheet(from_date=from_date, to_date=to_date)
    return render(request, 'timesheets/home.html', context)


@login_required
def employees_list(request):
    employees = Employee.objects
    context = {
        'employees': employees,
    }
    return render(request, 'timesheets/employees.html', context)


class TimeSheetView(ListView):
    model = TimeRecord
    template_name = "timesheets/home.html"

    def get_context_data(self):
        context = super().get_context_data()
        context.update(get_timesheet(**self.kwargs))

        return context


class SubProjectListView(ListView):
    model = SubProject

    def get_queryset(self):
        qs = super().get_queryset()
        if 'project' in self.kwargs and self.kwargs['project'] is not None:
            qs = qs.filter(parent_project=self.kwargs['project'])

        return qs


class ProjectListView(ListView):
    model = Project


class TimeRecordNewView(FormView):
    template_name = 'timesheets/timerecord_edit.html'
    form_class = TimeRecordForm
    initial = {
        'hours': 1.0,
        'date': date.today(),
    }
    success_url = '/timesheets'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create'

        return context

    def get_initial(self):
        self.initial['employee'] = self.request.user.employee
        return self.initial


class TimeRecordEditView(UpdateView):
    template_name = 'timesheets/timerecord_edit.html'
    model = TimeRecord
    form_class = TimeRecordForm
    success_url = '/timesheets'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'modify'

        return context


class SubProjectFormView(FormView):
    template_name = 'timesheets/subproject_edit.html'
    form_class = SubProjectForm
    success_url = 'timesheets/subproject_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create'
        if 'timerecord_id' in self.kwargs:
            context['action'] = 'modify'

        return context

    def get_initial(self):
        self.initial['employee'] = self.request.user.employee
        return self.initial


class ProjectFormView(FormView):
    template_name = 'timesheets/project_edit.html'
    form_class = ProjectForm
    success_url = '/timesheets/project_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create'
        if 'timerecord_id' in self.kwargs:
            context['action'] = 'modify'

        return context

    def get_initial(self):
        self.initial['employee'] = self.request.user.employee
        return self.initial


class TimeRecordDeleteView(DeleteView):
    model = TimeRecord
    success_url = '/timesheets/'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):

        response = super().dispatch(*args, **kwargs)
        if self.request.is_ajax():
            response_data = {"result": "ok"}
            return HttpResponse(json.dumps(response_data), content_type="application/json")

        else:
            return response
