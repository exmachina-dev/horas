from django.conf.urls import patterns, url

from .views import HomeView
from .views import TimeSheetView, SubProjectListView, ProjectListView
from .views import SubProjectFormView, ProjectFormView
from .views import TimeRecordNewView, TimeRecordEditView, TimeRecordDeleteView

urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^by_employee/(?P<employee>\w{1,4})/$', TimeSheetView.as_view(), name='timesheet_by_employee'),

    #url(r'^timesheet/(?:by_subproject/(?P<subproject>)/)?(?:by_project/(?P<project>\d+)/)?$', TimeSheetView.as_view(), name='timesheet_view'),
    url(r'^subprojects/(?:by_project/(?P<project>\d+)/)?$', SubProjectListView.as_view(), name='subproject_list'),
    url(r'^projects$', ProjectListView.as_view(), name='project_list'),

    url(r'^timerecord/new$', TimeRecordNewView.as_view(), name='new_timerecord'),
    url(r'^timerecord/(?P<pk>\d+)/$', TimeRecordEditView.as_view(), name='edit_timerecord'),
    url(r'^timerecord/(?P<pk>\d+)/delete$', TimeRecordDeleteView.as_view(), name='delete_timerecord'),

    url(r'^supbroject/new$', SubProjectFormView.as_view(), name='new_subproject'),
    url(r'^supbroject/(?P<pk>\d+)/$', SubProjectFormView.as_view(), name='edit_subproject'),

    url(r'^project/new$', ProjectFormView.as_view(), name='new_project'),
    url(r'^project/(?P<pk>\d+)/$', ProjectFormView.as_view(), name='edit_project'),
)
