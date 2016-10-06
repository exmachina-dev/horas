# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0026_auto_20160916_1434'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='id',
        ),
        migrations.AlterField(
            model_name='project',
            name='initials',
            field=models.CharField(primary_key=True, serialize=False, max_length=10),
            preserve_default=True,
        ),
    ]
