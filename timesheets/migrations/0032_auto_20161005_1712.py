# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0031_auto_20161005_0910'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='user',
        ),
        migrations.DeleteModel(
            name='Employee',
        ),
        migrations.AlterUniqueTogether(
            name='subproject',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='subproject',
            name='category',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.RemoveField(
            model_name='subproject',
            name='parent_project',
        ),
        migrations.DeleteModel(
            name='Project',
        ),
        migrations.DeleteModel(
            name='SubProject',
        ),
        migrations.DeleteModel(
            name='Task',
        ),
    ]
