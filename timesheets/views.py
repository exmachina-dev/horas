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

import json


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


class HomeView(LoginRequiredMixin, FormView):
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
        from_date = self.kwargs.get('form_date', date.today()-timedelta(days=7))
        to_date = self.kwargs.get('to_date', date.today())
        if not self.request.user.has_perm('view_from_all'):
            context.update(get_timesheet(
                from_date=from_date, to_date=to_date,
                employee=self.request.user.username))
        else:
            context.update(get_timesheet(from_date=from_date, to_date=to_date))

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

    def get_queryset(self):
        qs = super().get_queryset()
        if 'project' in self.kwargs and self.kwargs['project'] is not None:
            qs = qs.filter(parent_project=self.kwargs['project'])

        return qs


class ProjectListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Project
    permission_required = 'timesheets.view_project_list'


class TimeRecordNewView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'timesheets/timerecord_edit.html'
    form_class = TimeRecordForm
    initial = {
        'hours': 1.0,
        'date': date.today(),
    }
    success_url = '/timesheets'
    permission_required = 'timesheets.create_timerecord'
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
            return self.request.user.has_perm('timesheets.create_attached_timerecord')
        return initial_result

    def post(self, request, *args, **kwargs):
        # Catch any rules before post
        tr_employee = get_user_model().objects.get(pk=self.request.POST['employee']).employee
        if not tr_employee == self.request.user.employee and \
                not self.request.user.has_perm('timesheet.create_attached_timerecord'):
            messages.add_message(request, messages.ERROR, self.get_permission_denied_message())
            return redirect(self.request.META['HTTP_REFERER'])
        return super().post(request, *args, **kwargs)


class TimeRecordEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'timesheets/timerecord_edit.html'
    model = TimeRecord
    form_class = TimeRecordForm
    success_url = '/timesheets'
    permission_required = 'timesheets.change_timerecord'
    permission_denied_message = 'You don\'t have the permission to edit timerecords.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'modify'

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


class SubProjectFormView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'timesheets/subproject_edit.html'
    form_class = SubProjectForm
    model = SubProject
    success_url = 'timesheets/subproject_list.html'
    permission_required = 'timesheets.change_subproject'
    permission_denied_message = 'You don\'t have the permission to edit subprojects.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create'
        if 'timerecord_id' in self.kwargs:
            context['action'] = 'modify'

        return context

    def get_initial(self):
        self.initial = super().get_initial()
        self.initial['employee'] = self.request.user.employee
        return self.initial


class ProjectFormView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'timesheets/project_edit.html'
    form_class = ProjectForm
    success_url = '/timesheets/project_list.html'
    model = Project
    permission_required = 'timesheets.change_project'
    permission_denied_message = 'You don\'t have the permission to edit projects.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create'
        if 'timerecord_id' in self.kwargs:
            context['action'] = 'modify'

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
