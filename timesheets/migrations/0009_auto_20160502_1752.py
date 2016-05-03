# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0008_project_analytic_code'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='timerecord',
            options={'permissions': (('view_from_all', 'Can view timerecords attached to other employees'), ('create_attached_timerecord', 'Can create timerecords attached to the logged-in user'), ('change_attached_timerecord', 'Can edit timerecords attached to the logged-in user'), ('delete_attached_timerecord', 'Can delete timerecords attached to the logged-in user')), 'ordering': ('project', 'date', 'employee')},
        ),
    ]
