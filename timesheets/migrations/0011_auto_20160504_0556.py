# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0010_auto_20160502_1801'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'permissions': (('view_subproject_list', 'Can view subprojects list'),)},
        ),
        migrations.AlterModelOptions(
            name='subproject',
            options={'permissions': (('view_subproject_list', 'Can view subprojects list'),)},
        ),
    ]
