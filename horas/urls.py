from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout

import timesheets.urls

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'horas.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'horas.views.home', name='home'),

    url(r'^timesheets/', include(timesheets.urls, namespace='timesheets')),

    url(r'^login$', login),
    url(r'^logout$', logout, name='logout'),
)
