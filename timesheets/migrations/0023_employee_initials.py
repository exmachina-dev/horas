# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0022_auto_20160909_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='initials',
            field=models.CharField(null=True, unique=True, max_length=5),
            preserve_default=True,
        ),
    ]
