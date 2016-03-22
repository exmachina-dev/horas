from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'timesheets.views.home', name='home'),
)
