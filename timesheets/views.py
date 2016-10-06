# from django.contrib.auth.mixins import LoginRequiredMixin # New in Django 1.9
from django.http import HttpResponse
from django.db.models import Sum
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework import filters

from .models import TimeRecord
from projects.models import Project
from users.models import Employee
from tasks.models import Task
from .forms import TimeRecordForm

#from .serializers import TimeRecordSerializer
from utils.auth_mixins import LoginRequiredMixin, PermissionRequiredMixin

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
        projects = Project.objects.get(pk=kwargs.get('project')).projects
    else:
        projects = Project.objects.all()

    category = kwargs.get('category')

    date_span = (to_date - from_date).days
    day_range = [to_date - timedelta(days=x) for x in range(0, date_span + 1)]
    day_range.reverse()

    if kwargs.get('is_closed') is not None:
        projects = projects.filter(is_closed=kwargs.get('is_closed'))
    else:
        projects = projects.filter(is_closed=False)

    employees = employees.order_by('user__username')
    projects = projects.order_by('parent_project', 'initials')

    bow = from_date - timedelta(days=from_date.weekday())
    eow = from_date + timedelta(days=7 - from_date.isoweekday())
    from_jogline = {
        'beginning_of_week': bow,
        'previous_eow': bow - timedelta(days=1),
        'previous_week': bow - timedelta(days=7),
        'previous_month': bow - timedelta(days=calendar.monthrange(
            from_date.year if from_date.month > 1 else from_date.year-1,
            from_date.month-1 if from_date.month > 1 else 12)[1]),
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
        'previous_month': eow - timedelta(days=calendar.monthrange(
            from_date.year if from_date.month > 1 else from_date.year-1,
            from_date.month-1 if from_date.month > 1 else 12)[1]),
        'next_eow': eow + timedelta(days=7),
        'next_week': bow + timedelta(days=7),
        'next_month': eow + timedelta(days=calendar.monthrange(from_date.year, from_date.month)[1]),
        'end_of_week': eow,
    }

    timesheet = []

    for project in projects:
        project_tr = project.parent_project.timerecords.filter(date__range=(from_date, to_date), employee__in=employees).order_by('date')
        project_tr = project_tr.filter(project=project).order_by('date')
        cur_date = from_date
        project_ts = []
        while cur_date <= to_date:
            date_tr = project_tr.filter(date=cur_date)
            hours_by_project = project_tr.filter(date=cur_date).aggregate(Sum('hours'))['hours__sum'] or None
            project_ts.append({
                'date': cur_date,
                'timerecords': date_tr.order_by('employee'),
                'total_hours_by_project': date_tr.aggregate(Sum('hours'))['hours__sum'] or None,
                'total_hours_by_project': hours_by_project,
            })
            cur_date = cur_date + timedelta(days=1)
        timesheet.append({
            'project': project,
            'total_hours_by_project': project_tr.aggregate(Sum('hours'))['hours__sum'] or None,
            'timesheet': project_ts,
            'project': project.parent_project,
            'total_hours_by_project': project.parent_project.timerecords.filter(date__range=(from_date, to_date), employee__in=employees).aggregate(Sum('hours'))['hours__sum'] or None,
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
        'projects': projects,
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
    template_name = 'timesheets/timesheet.html'
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
        if 'previous_subproject' in self.request.session:
            self.initial['project'] = self.request.session['previous_subproject']

        return self.initial

    def post(self, request, *args, **kwargs):
        request.session['previous_subproject'] = request.POST['project']
        return super().post(request, *args, **kwargs)


class EmployeeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Employee


class TimeSheetView(LoginRequiredMixin, ListView):
    model = TimeRecord
    template_name = 'timesheets/timesheet.html'

    def get_context_data(self):
        context = super().get_context_data()
        context.update(get_timesheet(**self.kwargs))

        return context


class ProjectListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Project
    permission_required = 'timesheets.view_project_list'
    permission_denied_message = 'You don\'t have the permission to project list.'

    def get_queryset(self):
        qs = super().get_queryset()
        if 'finished' in self.kwargs and self.kwargs['finished'] is not None:
            qs = qs.filter(finished=self.kwargs['finished'])

        qs = qs.order_by('initials')
        return qs


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

    def get(self, request, *args, **kwargs):
        # Catch any rules before post
        tr_object = TimeRecord.objects.get(pk=self.kwargs['pk'])
        tr_employee = tr_object.employee
        if not tr_employee == self.request.user.employee and \
                not self.request.user.has_perm('timesheet.change_attached_timerecord'):
            messages.add_message(request, messages.ERROR, self.get_permission_denied_message())
            if not self.request.is_ajax():
                return redirect(self.request.META['HTTP_REFERER'])
        return super().get(request, *args, **kwargs)


#class TimeRecordViewSet(viewsets.ModelViewSet):
#    queryset = TimeRecord.objects.all()
#    serializer_class = TimeRecordSerializer
#    filter_backends = (filters.DjangoFilterBackend,)
#    filter_fields = ('project', 'task')
#
#
#class SubProjectViewSet(viewsets.ModelViewSet):
#    lookup_field = 'initials'
#    queryset = SubProject.objects.order_by('parent_project__initials', 'initials')
#    serializer_class = SubProjectSerializer
#    filter_backends = (filters.DjangoFilterBackend,)
#    filter_fields = ('parent_project', 'finished')
#
#
#class ProjectViewSet(viewsets.ModelViewSet):
#    lookup_field = 'initials'
#    queryset = Project.objects.order_by('initials')
#    serializer_class = ProjectSerializer
#    filter_fackends = (filters.DjangoFilterBackend,)
#
#
#class CategoryViewSet(viewsets.ModelViewSet):
#    queryset = Category.objects.order_by('name')
#    serializer_class = CategorySerializer
#
#
#class TaskViewSet(viewsets.ModelViewSet):
#    lookup_field = 'initials'
#    queryset = Task.objects.order_by('initials')
#    serializer_class = TaskSerializer
#
#
#class EmployeeViewSet(viewsets.ModelViewSet):
#    lookup_field = 'user__username'
#    queryset = Employee.objects.filter(user__is_active=True).order_by('user__username')
#    serializer_class = EmployeeSerializer
#    filter_backends = (filters.DjangoFilterBackend,)
