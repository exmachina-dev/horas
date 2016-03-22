from django.contrib import admin

# Register your models here.
from .models import Project, SubProject, Employee

admin.site.register(Project)
admin.site.register(SubProject)
admin.site.register(Employee)
