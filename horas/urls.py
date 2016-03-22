from django.conf.urls import patterns, include, url
from django.contrib import admin

import timesheets.urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'horas.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'horas.views.home', name='home'),
    url(r'^timesheets$', include(timesheets.urls)),
)
