from django.conf.urls import patterns, url

from .views import SubProjectListView, ProjectListView
from .views import TimeRecordFormView, SubProjectFormView, ProjectFormView

urlpatterns = patterns(
    '',
    url(r'^$', 'timesheets.views.home', name='home'),
    url(r'^by_employee/(?P<employee>\w{1,4})/$', 'timesheets.views.timesheet', name='timesheet_by_employee'),

    url(r'^timesheet/(?:by_subproject/(?P<subproject>)/)?(?:by_project/(?P<project>\d+)/)?$', SubProjectListView.as_view(), name='subproject_list'),
    url(r'^subprojects/(?:by_project/(?P<project>\d+)/)?$', SubProjectListView.as_view(), name='subproject_list'),
    url(r'^projects$', ProjectListView.as_view(), name='project_list'),

    url(r'^timerecord/new$', TimeRecordFormView.as_view(), name='new_timerecord'),
    url(r'^timerecord/(?P<timerecord>\d+)/$', TimeRecordFormView.as_view(), name='edit_timerecord'),

    url(r'^supbroject/new$', SubProjectFormView.as_view(), name='new_subproject'),
    url(r'^supbroject/(?P<subproject>\d+)/$', SubProjectFormView.as_view(), name='edit_subproject'),

    url(r'^project/new$', ProjectFormView.as_view(), name='new_project'),
    url(r'^project/(?P<project>\d+)/$', ProjectFormView.as_view(), name='edit_project'),
)
