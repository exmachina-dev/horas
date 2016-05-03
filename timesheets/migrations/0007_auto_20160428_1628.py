# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0006_auto_20160411_1941'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='timerecord',
            options={'ordering': ('project', 'date', 'employee'), 'permissions': (('view_from_all', 'Can view timerecords attached to other employees'),)},
        ),
    ]
