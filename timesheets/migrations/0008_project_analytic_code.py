# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0007_auto_20160428_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='analytic_code',
            field=models.CharField(max_length=30, blank=True),
            preserve_default=True,
        ),
    ]
