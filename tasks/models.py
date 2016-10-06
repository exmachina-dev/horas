from django.db import models

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)
    project = models.ForeignKey('projects.Project')
    assignees = models.ManyToManyField('users.Employee', blank=True)
    prerequisite_tasks = models.ManyToManyField('self', blank=True)
    begin_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    assigned_hours = models.FloatField(null=True, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.project.get_full_initials(), self.name)
