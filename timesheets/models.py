from django.db import models

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=30)
    initials = models.CharField(max_length=5)

class SubProject(Project):
    parent_project = models.ForeignKey(Project, blank=True, null=True)

class Timeline(models.Model):
    employee = models.ForeignKey(User)
    date = models.DateField()
    hours = models.FloatField()
    project = models.ForeignKey(Project)
    
