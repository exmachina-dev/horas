# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0011_auto_20160504_0556'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'permissions': (('view_project_list', 'Can view project list'),)},
        ),
        migrations.AlterModelOptions(
            name='subproject',
            options={'permissions': (('view_subproject_list', 'Can view subproject list'),)},
        ),
    ]
