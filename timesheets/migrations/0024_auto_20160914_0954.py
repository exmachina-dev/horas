# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0023_employee_initials'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='id',
        ),
        migrations.AlterField(
            model_name='employee',
            name='initials',
            field=models.CharField(serialize=False, primary_key=True, max_length=5),
            preserve_default=True,
        ),
    ]
