from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout

import home.urls
import projects.urls
import tasks.urls
import timesheets.urls

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'horas.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'home.views.home', name='home'),

    url(r'^projects/', include(projects.urls, namespace='projects')),
    url(r'^tasks/', include(tasks.urls, namespace='tasks')),
    url(r'^timesheets/', include(timesheets.urls, namespace='timesheets')),

    url('^', include('django.contrib.auth.urls'))
)
