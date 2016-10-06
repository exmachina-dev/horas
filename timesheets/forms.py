from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import TimeRecord


class TimeRecordForm(ModelForm):
    class Meta:
        model = TimeRecord
        fields = ['employee', 'date', 'task', 'hours']

    def clean_project(self):
        task = self.cleaned_data['task']
        if task.parent_project.is_closed:
            raise ValidationError({'task': 'Project is closed.'})
        return project
