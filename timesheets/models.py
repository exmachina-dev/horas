from django.db import models
from django.conf import settings

import math
import random

# Create your models here.


class TimeRecordManager(models.Manager):
    def by_date(self, date):
        return self.filter(date=date)

    def hours_by_project_and_date(self, project, date):
        total = 0
        for hour in self.filter(project=project, date=date):
            total += hour
            return total


class TimeRecord(models.Model):
    employee = models.ForeignKey('users.Employee', limit_choices_to={'is_active': True})
    date = models.DateField()
    hours = models.FloatField(default=0)
    task = models.ForeignKey('tasks.Task', on_delete=models.CASCADE,
    related_name='parent_task')
    objects = TimeRecordManager()

    class Meta(object):
        ordering = ('date', 'task', 'employee',)
        unique_together = ('task', 'date', 'employee')
        permissions = (
            ('view_from_all', 'Can view timerecords attached to other employees'),
            ('create_attached_timerecord', 'Can create timerecords attached to the user'),
            ('change_attached_timerecord', 'Can edit timerecords attached to the user'),
            ('delete_attached_timerecord', 'Can delete timerecords attached to the user'),
        )

    @property
    def formatted_hours(self):
        h = int(math.floor(self.hours))
        m = int((self.hours - h) * 60)
        return '{:d}h{:02d}'.format(h, m)

    def __str__(self):
        return '{} - {!s} - {} ({:.2f})'.format(self.task, self.date,
                self.employee.initials, self.hours)
