from django.db import models
from django.conf import settings

import math

# Create your models here.


class Employee(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text="User binded to this employee")
    color = models.CharField(
        max_length=25, default="#af0000",
        help_text="Color in CSS format (hexadecimal or rgb format)")

    def __str__(self):
        return '{}'.format(self.user.username)


class TimeRecordManager(models.Manager):
    def by_date(self, date):
        return self.filter(date=date)

    def hours_by_project_and_date(self, project, date):
        total = 0
        for hour in self.filter(project=project, date=date):
            total += hour
            return total


class TimeRecord(models.Model):
    employee = models.ForeignKey('Employee')
    date = models.DateField()
    hours = models.FloatField()
    project = models.ForeignKey('SubProject')
    objects = TimeRecordManager()

    class Meta(object):
        ordering = ('project', 'date', 'employee',)
        unique_together = ('project', 'date', 'employee')

    @property
    def formatted_hours(self):
        h = int(math.floor(self.hours))
        m = int((self.hours - h) * 60)
        return '{:d}h{:02d}'.format(h, m)

    def __str__(self):
        return '{!s} - {} - {!s}'.format(self.project, self.date, self.employee)


class SubProjectManager(models.Manager):
    pass

    def timerecords_by_date(self, date):
        return self.timerecords.filter(date=date).order_by('date')


class SubProject(models.Model):
    initials = models.CharField(max_length=5)
    name = models.CharField(max_length=30)
    analytic_code = models.CharField(max_length=30, blank=True)
    parent_project = models.ForeignKey('Project', blank=True, null=True)
    finished = models.BooleanField(default=False)
    objects = SubProjectManager()

    class Meta:
        unique_together = ('initials', 'parent_project')

    @property
    def timerecords(self):
        return TimeRecord.objects.filter(project=self)

    def total_hours(self):
        return self.timerecords.aggregate(models.Sum('hours'))['hours__sum']

    def __str__(self):
        if self.parent_project:
            return '{0.parent_project.initials}-{0.initials} - {0.name}'.format(self)
        return '{} - {}'.format(self.initials, self.name)


class Project(models.Model):
    initials = models.CharField(unique=True, max_length=5)
    name = models.CharField(max_length=30)

    @property
    def subprojects(self):
        return SubProject.objects.filter(parent_project=self)

    @property
    def timerecords(self):
        return TimeRecord.objects.filter(project=self.subprojects)

    def total_hours(self):
        return self.timerecords.aggregate(models.Sum('hours'))['hours__sum']

    def __str__(self):
        return '{} - {}'.format(self.initials, self.name)
