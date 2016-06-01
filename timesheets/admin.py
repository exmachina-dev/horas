from django.contrib import admin

# Register your models here.
from .models import Category, Project, SubProject, Employee, TimeRecord

admin.site.register(TimeRecord)
admin.site.register(SubProject)
admin.site.register(Project)
admin.site.register(Category)
admin.site.register(Employee)
