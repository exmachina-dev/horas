# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0027_auto_20160916_1444'),
        ('tasks', '0003_auto_20161003_1621'),
        ('users', '0003_auto_20161003_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timerecord',
            name='employee',
            field=models.ForeignKey(to='users.Employee'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timerecord',
            name='hours',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timerecord',
            name='project',
            field=models.ForeignKey(null=True, to='timesheets.SubProject'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timerecord',
            name='task',
            field=models.ForeignKey(to='tasks.Task', related_name='parent_task', default=0),
            preserve_default=False,
        ),
    ]
