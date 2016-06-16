# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0019_auto_20160607_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subproject',
            name='assigned_hours',
            field=models.FloatField(blank=0.0, default=0.0),
            preserve_default=True,
        ),
    ]
