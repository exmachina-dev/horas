# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0018_auto_20160601_0751'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subproject',
            options={'ordering': ('parent_project__initials', 'initials'), 'permissions': (('view_subproject_list', 'Can view subproject list'), ('view_assigned_hours', 'Can view assigned hours'))},
        ),
        migrations.AddField(
            model_name='subproject',
            name='assigned_hours',
            field=models.FloatField(default=0.0, blank=0.0),
            preserve_default=False,
        ),
    ]
