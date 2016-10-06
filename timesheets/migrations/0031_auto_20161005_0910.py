# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0030_auto_20161005_0909'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='timerecord',
            options={'ordering': ('project', 'date', 'employee'), 'permissions': (('view_from_all', 'Can view timerecords attached to other employees'), ('create_attached_timerecord', 'Can create timerecords attached to the user'), ('change_attached_timerecord', 'Can edit timerecords attached to the user'), ('delete_attached_timerecord', 'Can delete timerecords attached to the user'))},
        ),
        migrations.RenameField(
            model_name='timerecord',
            old_name='project2',
            new_name='project',
        ),
        migrations.AlterUniqueTogether(
            name='timerecord',
            unique_together=set([('project', 'date', 'task', 'employee')]),
        ),
    ]
