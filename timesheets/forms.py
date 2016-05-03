from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import TimeRecord, Project, SubProject


class TimeRecordForm(ModelForm):
    class Meta:
        model = TimeRecord
        fields = ['employee', 'date', 'project', 'hours']

    def clean_project(self):
        project = self.cleaned_data['project']
        print(project)
        print(project.finished)
        if project.finished:
            raise ValidationError({'project': 'Project is finished.'})
        return project


class SubProjectForm(ModelForm):
    class Meta:
        model = SubProject
        fields = ['initials', 'name', 'parent_project', 'analytic_code', 'finished']


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['initials', 'name', 'analytic_code']
