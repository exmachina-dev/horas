# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20161003_1556'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='assigned_hours',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='begin_date',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='end_date',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
    ]
