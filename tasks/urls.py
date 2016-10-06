from django.conf.urls import patterns, url, include

from .views import HomeView, TaskListView

urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^list/$', TaskListView.as_view(), name='task_list'),
)

