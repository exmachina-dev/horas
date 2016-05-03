from django.forms import ModelForm
from .models import TimeRecord, Project, SubProject


class TimeRecordForm(ModelForm):
    class Meta:
        model = TimeRecord
        fields = ['employee', 'date', 'project', 'hours']


class SubProjectForm(ModelForm):
    class Meta:
        model = SubProject
        fields = ['initials', 'name', 'parent_project', 'analytic_code', 'finished']


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['initials', 'name', 'analytic_code']
