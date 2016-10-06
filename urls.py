from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout

from rest_framework import routers

import projects.urls
import tasks.urls
import timesheets.urls

rest_router = routers.DefaultRouter()
#rest_router.register(r'projects', ProjectViewSet)
#rest_router.register(r'timesheets', EmployeeViewSet)
#rest_router.register(r'categories', CategoryViewSet)

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'horas.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'views.home', name='home'),

    url(r'^projects/', include(projects.urls, namespace='projects')),
    url(r'^tasks/', include(tasks.urls, namespace='tasks')),
    url(r'^timesheets/', include(timesheets.urls, namespace='timesheets')),

    url('^', include('django.contrib.auth.urls')),

    url(r'^api/auth', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(rest_router.urls)),
)
