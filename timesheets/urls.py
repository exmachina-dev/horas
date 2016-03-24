from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'timesheets.views.home', name='home'),
    url(r'^by_employee/(?P<employee>\w{1,4})/$', 'timesheets.views.timesheet', name='timesheet_by_employee'),
)
