# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0025_employee_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='is_active',
            field=models.BooleanField(help_text='Wether the employee is active in the company or not.', default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subproject',
            name='parent_project',
            field=models.ForeignKey(default=0, to='timesheets.Project'),
            preserve_default=True,
        ),
    ]
