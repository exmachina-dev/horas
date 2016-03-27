from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.views.generic.edit import FormView
from django.views.generic import ListView

from .models import Employee, SubProject, Project
from .forms import TimeRecordForm, SubProjectForm, ProjectForm

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


class SubProjectListView(ListView):
    model = SubProject

    def get_queryset(self):
        qs = super().get_queryset()
        if 'project' in self.kwargs:
            qs = qs.filter(parent_project=self.kwargs['project'])

        return qs


class ProjectListView(ListView):
    model = Project


class TimeRecordFormView(FormView):
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
        if 'timerecord_id' in self.kwargs:
            context['action'] = 'modify'

        return context

    def get_initial(self):
        self.initial['employee'] = self.request.user.employee
        return self.initial


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
