# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0017_auto_20160601_0746'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subproject',
            options={'permissions': (('view_subproject_list', 'Can view subproject list'),), 'ordering': ('parent_project__initials', 'initials')},
        ),
        migrations.RemoveField(
            model_name='subproject',
            name='full_initials',
        ),
    ]
