# from django.contrib.auth.mixins import LoginRequiredMixin # New in Django 1.9
from django.http import HttpResponse
from django.db.models import Sum
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import get_user_model

from .models import TimeRecord, Employee, SubProject, Project
from .forms import TimeRecordForm, SubProjectForm, ProjectForm

from .auth_mixins import LoginRequiredMixin, PermissionRequiredMixin

from datetime import date
from datetime import timedelta
from datetime import datetime

import calendar

import json


def get_timesheet(**kwargs):
    filter_by = list()
    employees = kwargs.get('employees')
    if employees:
        employees = Employee.objects.filter(user__username__in=employees.split(','))
        filter_by.append('employee')
    else:
        employees = Employee.objects.all()

    from_date = kwargs.get('from_date', date.today() - timedelta(days=date.today().weekday()))
    to_date = kwargs.get('to_date', from_date + timedelta(days=6))

    if kwargs.get('project'):
        subprojects = Project.objects.get(pk=kwargs.get('project')).subprojects
    elif kwargs.get('subproject'):
        subprojects = SubProject.objects.filter(pk=kwargs.get('subproject'))
    else:
        subprojects = SubProject.objects.all()
    date_span = (to_date - from_date).days
    day_range = [to_date - timedelta(days=x) for x in range(0, date_span + 1)]
    day_range.reverse()

    employees = employees.order_by('user__username')
    subprojects = subprojects.order_by('parent_project')

    bow = from_date - timedelta(days=from_date.weekday())
    eow = from_date + timedelta(days=7 - from_date.isoweekday())
    from_jogline = {
        'beginning_of_week': bow,
        'previous_eow': bow - timedelta(days=1),
        'previous_week': bow - timedelta(days=7),
        'previous_month': bow - timedelta(days=calendar.monthrange(from_date.year, from_date.month-1)[1]),
        'next_eow': eow + timedelta(days=1),
        'next_week': bow + timedelta(days=7),
        'next_month': bow + timedelta(days=calendar.monthrange(from_date.year, from_date.month)[1]),
        'end_of_week': eow,
    }

    bow = to_date - timedelta(days=to_date.weekday())
    eow = to_date + timedelta(days=7 - to_date.isoweekday())
    to_jogline = {
        'beginning_of_week': bow,
        'previous_eow': bow - timedelta(days=1),
        'previous_week': eow - timedelta(days=7),
        'previous_month': eow - timedelta(days=calendar.monthrange(from_date.year, from_date.month-1)[1]),
        'next_eow': eow + timedelta(days=7),
        'next_week': bow + timedelta(days=7),
        'next_month': eow + timedelta(days=calendar.monthrange(from_date.year, from_date.month)[1]),
        'end_of_week': eow,
    }

    timesheet = []

    for subproject in subprojects:
        project_tr = subproject.parent_project.timerecords.filter(date__range=(from_date, to_date), employee__in=employees).order_by('date')
        subproject_tr = project_tr.filter(project=subproject).order_by('date')
        cur_date = from_date
        subproject_ts = []
        while cur_date <= to_date:
            date_tr = subproject_tr.filter(date=cur_date)
            hours_by_project = project_tr.filter(date=cur_date).aggregate(Sum('hours'))['hours__sum'] or None
            subproject_ts.append({
                'date': cur_date,
                'timerecords': date_tr.order_by('employee'),
                'total_hours_by_subproject': date_tr.aggregate(Sum('hours'))['hours__sum'] or None,
                'total_hours_by_project': hours_by_project,
            })
            cur_date = cur_date + timedelta(days=1)
        timesheet.append({
            'subproject': subproject,
            'total_hours_by_subproject': subproject_tr.aggregate(Sum('hours'))['hours__sum'] or None,
            'timesheet': subproject_ts,
            'project': subproject.parent_project,
            'total_hours_by_project': subproject.parent_project.timerecords.filter(date__range=(from_date, to_date), employee__in=employees).aggregate(Sum('hours'))['hours__sum'] or None,
        })

    cur_date = from_date
    total_hours_ts = []
    while cur_date <= to_date:
        hours_by_employee = []
        total_hours_by_day = TimeRecord.objects.filter(date=cur_date).aggregate(Sum('hours'))['hours__sum'] or None
        for employee in employees:
            timerecord_qs = TimeRecord.objects.filter(date=cur_date, employee=employee).order_by('eemployee')
            hours = timerecord_qs.aggregate(Sum('hours'))['hours__sum'] or None
            if hours != 0:
                hours_by_employee.append({
                    'employee': employee,
                    'total_hours': hours,
                })

        total_hours_ts.append({
            'hours_by_employee': hours_by_employee,
            'total_hours_by_day': total_hours_by_day,
        })

        cur_date = cur_date + timedelta(days=1)

    context = {
        'filter_by': filter_by,
        'employees': employees.order_by('user__username'),
        'subprojects': subprojects,
        'days': day_range,
        'timesheet': timesheet,
        'total_hours': total_hours_ts,
        'total': TimeRecord.objects.filter(date__range=(from_date, to_date), employee__in=employees).aggregate(Sum('hours'))['hours__sum'] or 0,
        'start_date': from_date,
        'end_date': to_date,
        'start_jogline': from_jogline,
        'end_jogline': to_jogline,
    }

    return context


class HomeView(LoginRequiredMixin, CreateView):
    template_name = 'timesheets/home.html'
    form_class = TimeRecordForm
    initial = {
        'hours': 1.0,
        'date': date.today(),
    }

    model = TimeRecord
    form_class = TimeRecordForm
    success_url = '/timesheets'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ts_kwargs = {
            'project': self.kwargs.get('project'),
            'subproject': self.kwargs.get('subproject'),
            'employees': self.kwargs.get('employees'),
        }
        if self.kwargs.get('from_date'):
            ts_kwargs.update({'from_date': datetime.strptime(self.kwargs.get('from_date'), '%Y%m%d')})
        if self.kwargs.get('to_date'):
            ts_kwargs.update({'to_date': datetime.strptime(self.kwargs.get('to_date'), '%Y%m%d')})

        if not self.request.user.has_perm('timesheets.view_from_all'):
            ts_kwargs.update({'employees': self.request.user.username})
        context.update(get_timesheet(**ts_kwargs))

        return context

    def get_initial(self):
        self.initial = super().get_initial()
        if hasattr(self.request.user, 'employee'):
            self.initial['employee'] = self.request.user.employee
        return self.initial


class EmployeeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Employee
    template_name = 'timesheets/employees.html'


class TimeSheetView(LoginRequiredMixin, ListView):
    model = TimeRecord
    template_name = "timesheets/home.html"

    def get_context_data(self):
        context = super().get_context_data()
        context.update(get_timesheet(**self.kwargs))

        return context


class SubProjectListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = SubProject
    permission_required = 'timesheets.view_subproject_list'
    permission_denied_message = 'You don\'t have the permission to view the subproject list.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'project' in self.kwargs and self.kwargs['project'] is not None:
            context['project'] = Project.objects.get(pk=self.kwargs['project'])
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        if 'project' in self.kwargs and self.kwargs['project'] is not None:
            qs = qs.filter(parent_project=self.kwargs['project'])

        return qs


class ProjectListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Project
    permission_required = 'timesheets.view_project_list'
    permission_denied_message = 'You don\'t have the permission to project list.'


class TimeRecordNewView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'timesheets/timerecord_edit.html'
    form_class = TimeRecordForm
    initial = {
        'hours': 1.0,
        'date': date.today(),
    }
    success_url = '/timesheets'
    permission_required = 'timesheets.add_timerecord'
    permission_denied_message = 'You don\'t have the permission to create timerecords.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create'

        return context

    def get_initial(self):
        self.initial = super().get_initial()
        if hasattr(self.request.user, 'employee'):
            self.initial['employee'] = self.request.user.employee

        return self.initial

    def has_permission(self):
        perms = self.get_permission_required()
        initial_result = self.request.user.has_perms(perms)

        if not initial_result:
            return self.request.user.has_perm('timesheets.add_attached_timerecord')
        return initial_result

    def post(self, request, *args, **kwargs):
        # Catch any rules before post
        tr_employee = get_user_model().objects.get(pk=self.request.POST['employee']).employee
        if not tr_employee == self.request.user.employee and \
                not self.request.user.has_perm('timesheet.create_attached_timerecord'):
            messages.add_message(request, messages.ERROR, self.get_permission_denied_message())
            return redirect(self.request.META['HTTP_REFERER'])
        return super().post(request, *args, **kwargs)


class SubProjectNewView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'timesheets/subproject_edit.html'
    form_class = SubProjectForm
    success_url = '/timesheets/subprojects'
    permission_required = 'timesheets.add_subproject'
    permission_denied_message = 'You don\'t have the permission to create subprojects.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create'

        return context


class ProjectNewView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'timesheets/project_edit.html'
    form_class = ProjectForm
    success_url = '/projects'
    permission_required = 'timesheets.add_project'
    permission_denied_message = 'You don\'t have the permission to create projects.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create'

        return context


class TimeRecordEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'timesheets/timerecord_edit.html'
    model = TimeRecord
    form_class = TimeRecordForm
    success_url = '/timesheets'
    permission_required = 'timesheets.change_timerecord'
    permission_denied_message = 'You don\'t have the permission to edit timerecords.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'update'

        return context

    def has_permission(self):
        perms = self.get_permission_required()
        initial_result = self.request.user.has_perms(perms)

        if not initial_result:
            return self.request.user.has_perm('timesheets.change_attached_timerecord')
        return initial_result

    def post(self, request, *args, **kwargs):
        # Catch any rules before post
        tr_employee = get_user_model().objects.get(pk=self.request.POST['employee']).employee
        if not tr_employee == self.request.user.employee and \
                not self.request.user.has_perm('timesheet.change_attached_timerecord'):
            messages.add_message(request, messages.ERROR, self.get_permission_denied_message())
            return redirect(self.request.META['HTTP_REFERER'])
        return super().post(request, *args, **kwargs)


class SubProjectEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'timesheets/subproject_edit.html'
    form_class = SubProjectForm
    model = SubProject
    success_url = '/timesheets/subprojects'
    permission_required = 'timesheets.change_subproject'
    permission_denied_message = 'You don\'t have the permission to edit subprojects.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'update'

        return context

    def get_initial(self):
        self.initial = super().get_initial()
        self.initial['employee'] = self.request.user.employee
        return self.initial


class ProjectEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'timesheets/project_edit.html'
    form_class = ProjectForm
    success_url = '/timesheets/projects'
    model = Project
    permission_required = 'timesheets.change_project'
    permission_denied_message = 'You don\'t have the permission to edit projects.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'update'

        return context

    def get_initial(self):
        self.initial = super().get_initial()
        self.initial['employee'] = self.request.user.employee
        return self.initial


class TimeRecordDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = TimeRecord
    template_name = 'timesheets/confirm_delete.html'
    success_url = '/timesheets/'
    permission_required = 'timesheets.delete_timerecord'
    permission_denied_message = 'You don\'t have the permission to delete timerecords.'

    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        if self.request.is_ajax():
            response_data = {"result": "ok"}
            return HttpResponse(json.dumps(response_data), content_type="application/json")

        else:
            return response

    def has_permission(self):
        perms = self.get_permission_required()
        initial_result = self.request.user.has_perms(perms)

        if not initial_result:
            return self.request.user.has_perm('timesheets.delete_attached_timerecord')
        return initial_result

    def post(self, request, *args, **kwargs):
        # Catch any rules before post
        tr_employee = get_user_model().objects.get(pk=self.request.POST['employee']).employee
        if not tr_employee == self.request.user.employee and \
                not self.request.user.has_perm('timesheet.change_attached_timerecord'):
            messages.add_message(request, messages.ERROR, self.get_permission_denied_message())
            return redirect(self.request.META['HTTP_REFERER'])
        return super().post(request, *args, **kwargs)


class SubProjectDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = SubProject
    template_name = 'timesheets/confirm_delete.html'
    success_url = '/timesheets/'
    permission_required = 'timesheets.delete_subproject'
    permission_denied_message = 'You don\'t have the permission to delete subprojects.'

    def dispatch(self, *args, **kwargs):

        response = super().dispatch(*args, **kwargs)
        if self.request.is_ajax():
            response_data = {"result": "ok"}
            return HttpResponse(json.dumps(response_data), content_type="application/json")

        else:
            return response


class ProjectDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Project
    template_name = 'timesheets/confirm_delete.html'
    success_url = '/timesheets/'
    permission_required = 'timesheets.delete_project'
    permission_denied_message = 'You don\'t have the permission to delete projects.'

    def dispatch(self, *args, **kwargs):

        response = super().dispatch(*args, **kwargs)
        if self.request.is_ajax():
            response_data = {"result": "ok"}
            return HttpResponse(json.dumps(response_data), content_type="application/json")

        else:
            return response
