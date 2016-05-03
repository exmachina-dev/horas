# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0009_auto_20160502_1752'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='timerecord',
            options={'permissions': (('view_from_all', 'Can view timerecords attached to other employees'), ('create_attached_timerecord', 'Can create timerecords attached to the user'), ('change_attached_timerecord', 'Can edit timerecords attached to the user'), ('delete_attached_timerecord', 'Can delete timerecords attached to the user')), 'ordering': ('project', 'date', 'employee')},
        ),
    ]
