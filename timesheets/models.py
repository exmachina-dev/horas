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
        return '{!s} - {} - {!s}'.format(self.project, self.date, self.employee)


class SubProjectManager(models.Manager):
    pass

    def timerecords_by_date(self, date):
        return self.timerecords.filter(date=date).order_by('date')


class SubProject(models.Model):
    initials = models.CharField(max_length=10)
    name = models.CharField(max_length=30)
    analytic_code = models.CharField(max_length=30, blank=True)
    parent_project = models.ForeignKey('Project', blank=True, null=True)
    finished = models.BooleanField(default=False)
    category = models.ForeignKey('Category', blank=True, null=True)
    objects = SubProjectManager()

    class Meta:
        unique_together = ('initials', 'parent_project')
        ordering = ('parent_project__initials', 'initials',)
        permissions = (
            ('view_subproject_list', 'Can view subproject list'),
        )

    @property
    def timerecords(self):
        return TimeRecord.objects.filter(project=self)

    def total_hours(self):
        return self.timerecords.aggregate(models.Sum('hours'))['hours__sum']

    @property
    def uid(self):
        if self.parent_project:
            return '{0.parent_project.initials}-{0.initials}'.format(self)
        return '{}'.format(self.initials)

    def __str__(self):
        return '{0.uid} - {0.name}'.format(self)


class Project(models.Model):
    initials = models.CharField(unique=True, max_length=10)
    name = models.CharField(max_length=30)
    analytic_code = models.CharField(max_length=30, blank=True)
    finished = models.BooleanField(default=False)

    class Meta:
        permissions = (
            ('view_project_list', 'Can view project list'),
        )

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


class Category(models.Model):
    name = models.CharField(unique=True, max_length=30)
    description = models.CharField(max_length=100, blank=True)
    color = models.CharField(
        max_length=25, default="#af0000",
        help_text="Color in CSS format (hexadecimal or rgb format)")

    class Meta:
        verbose_name_plural = 'categories'
        permissions = (
            ('view_category_list', 'Can view category list'),
        )

    @property
    def subprojects(self):
        return SubProject.objects.filter(category=self)

    @property
    def timerecords(self):
        return TimeRecord.objects.filter(project=self.subprojects)

    def total_hours(self):
        return self.timerecords.aggregate(models.Sum('hours'))['hours__sum']

    def __str__(self):
        return '{}'.format(self.name)
