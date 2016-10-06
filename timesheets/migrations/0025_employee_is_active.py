# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0024_auto_20160914_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='is_active',
            field=models.BooleanField(help_text='Wether the employee is active en the company or not.', default=True),
            preserve_default=True,
        ),
    ]
