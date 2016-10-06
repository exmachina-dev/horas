from django.forms import ModelForm
from .models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'assignees', 'begin_date', 'end_date',
                'assigned_hours']
