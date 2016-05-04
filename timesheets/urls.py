from django.conf.urls import patterns, url

from .views import HomeView
from .views import TimeSheetView, SubProjectListView, ProjectListView
from .views import TimeRecordNewView, SubProjectNewView, ProjectNewView
from .views import TimeRecordEditView, SubProjectEditView, ProjectEditView
from .views import TimeRecordDeleteView, SubProjectDeleteView, ProjectDeleteView

urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^by_employee/(?P<employee>\w{1,4})/$', TimeSheetView.as_view(), name='timesheet_by_employee'),

    #url(r'^timesheet/(?:by_subproject/(?P<subproject>)/)?(?:by_project/(?P<project>\d+)/)?$', TimeSheetView.as_view(), name='timesheet_view'),
    url(r'^subprojects/(?:by_project/(?P<project>\d+)/)?$', SubProjectListView.as_view(), name='subproject_list'),
    url(r'^projects$', ProjectListView.as_view(), name='project_list'),

    url(r'^timerecord/new$', TimeRecordNewView.as_view(), name='timerecord_new'),
    url(r'^timerecord/(?P<pk>\d+)/$', TimeRecordEditView.as_view(), name='timerecord_edit'),
    url(r'^timerecord/(?P<pk>\d+)/delete$', TimeRecordDeleteView.as_view(), name='timerecord_delete'),

    url(r'^subproject/new$', SubProjectNewView.as_view(), name='subproject_new'),
    url(r'^subproject/(?P<pk>\d+)/$', SubProjectEditView.as_view(), name='subproject_edit'),
    url(r'^subproject/(?P<pk>\d+)/delete$', SubProjectDeleteView.as_view(), name='subproject_delete'),

    url(r'^project/new$', ProjectNewView.as_view(), name='project_new'),
    url(r'^project/(?P<pk>\d+)/$', ProjectEditView.as_view(), name='project_edit'),
    url(r'^project/(?P<pk>\d+)/delete$', ProjectDeleteView.as_view(), name='project_delete'),
)
