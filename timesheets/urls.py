from django.conf.urls import patterns, url

from .views import HomeView
from .views import TimeSheetView, SubProjectListView, ProjectListView, CategoryListView
from .views import TimeRecordNewView, SubProjectNewView, ProjectNewView, CategoryNewView
from .views import TimeRecordEditView, SubProjectEditView, ProjectEditView, CategoryEditView
from .views import TimeRecordDeleteView, SubProjectDeleteView, ProjectDeleteView, CategoryDeleteView

urlpatterns = patterns(
    '',
    url(r'^(?:from/(?P<from_date>\d{8})/)?(?:to/(?P<to_date>\d{8})/)?(?:by_category/(?P<category>\d+(?:,\d+)*)/)?(?:by_project/(?P<project>\d+)/)?(?:by_subproject/(?P<subproject>\d+)/)?(?:by_employee/(?P<employees>\w{1,4}(?:,\w{1,4})*)/)?$', HomeView.as_view(), name='home'),

    #url(r'^timesheet/(?:by_subproject/(?P<subproject>)/)?(?:by_project/(?P<project>\d+)/)?$', TimeSheetView.as_view(), name='timesheet_view'),
    url(r'^subprojects/(?:by_category/(?P<category>\d+)/)?(?:by_project/(?P<project>\d+)/)?$', SubProjectListView.as_view(), name='subproject_list'),
    url(r'^projects$', ProjectListView.as_view(), name='project_list'),
    url(r'^categories$', CategoryListView.as_view(), name='category_list'),

    url(r'^timerecord/new$', TimeRecordNewView.as_view(), name='timerecord_new'),
    url(r'^timerecord/(?P<pk>\d+)/$', TimeRecordEditView.as_view(), name='timerecord_edit'),
    url(r'^timerecord/(?P<pk>\d+)/delete$', TimeRecordDeleteView.as_view(), name='timerecord_delete'),

    url(r'^subproject/new/(?:with_project/(?P<project>\d+)/)?$', SubProjectNewView.as_view(), name='subproject_new'),
    url(r'^subproject/(?P<pk>\d+)/$', SubProjectEditView.as_view(), name='subproject_edit'),
    url(r'^subproject/(?P<pk>\d+)/delete$', SubProjectDeleteView.as_view(), name='subproject_delete'),

    url(r'^project/new$', ProjectNewView.as_view(), name='project_new'),
    url(r'^project/(?P<pk>\d+)/$', ProjectEditView.as_view(), name='project_edit'),
    url(r'^project/(?P<pk>\d+)/delete$', ProjectDeleteView.as_view(), name='project_delete'),

    url(r'^category/new$', CategoryNewView.as_view(), name='category_new'),
    url(r'^category/(?P<pk>\d+)/$', CategoryEditView.as_view(), name='category_edit'),
    url(r'^category/(?P<pk>\d+)/delete$', CategoryDeleteView.as_view(), name='category_delete'),
)
