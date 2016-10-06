# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0021_auto_20160909_1436'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='timerecord',
            unique_together=set([('project', 'date', 'task', 'employee')]),
        ),
    ]
