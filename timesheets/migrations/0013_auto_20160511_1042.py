# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0012_auto_20160504_0559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='initials',
            field=models.CharField(max_length=10, unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subproject',
            name='initials',
            field=models.CharField(max_length=10),
            preserve_default=True,
        ),
    ]
