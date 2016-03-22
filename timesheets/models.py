from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=30)
    initials = models.CharField(max_length=5)

class SubProject(models.Model):
    name = models.CharField(max_length=30)
    initials = models.CharField(max_length=5)
    parent_project = models.ForeignKey(Project, blank=True, null=True)

class Employee(models.Model):
    user = models.OneToOneField(User, unique=True)

class Timeline(models.Model):
    employee = models.ForeignKey(Employee)
    date = models.DateField()
    hours = models.FloatField()
    project = models.ForeignKey(Project)
    
