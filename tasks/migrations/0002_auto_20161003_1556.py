# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='assignees',
            field=models.ManyToManyField(to='users.Employee', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.CharField(blank=True, max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='prerequisite_tasks',
            field=models.ManyToManyField(to='tasks.Task', related_name='prerequisite_tasks_rel_+', blank=True),
            preserve_default=True,
        ),
    ]
