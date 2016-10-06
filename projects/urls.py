from django.conf.urls import patterns, url, include

from .views import HomeView, ProjectListView, ProjectNewView
from .views import ProjectEditView, ProjectDeleteView

urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^list/(?:project/(?P<project>\d+))?$', ProjectListView.as_view(), name='project_list'),
    url(r'^new/$', ProjectNewView.as_view(), name='project_new'),
    url(r'^edit/(?P<project>\d+)$', ProjectEditView.as_view(), name='project_edit'),
    url(r'^delete/(?P<project>\d+)$', ProjectDeleteView.as_view(),
        name='project_delete'),
)
