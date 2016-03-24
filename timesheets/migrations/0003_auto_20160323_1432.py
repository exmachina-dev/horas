# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0002_auto_20160323_0726'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='timerecord',
            options={'ordering': ('project', 'date', 'employee')},
        ),
        migrations.AddField(
            model_name='employee',
            name='color',
            field=models.CharField(max_length=7, default='#ffffff'),
            preserve_default=True,
        ),
    ]
