# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20161003_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='analytic_code',
            field=models.CharField(max_length=20, blank=True),
            preserve_default=True,
        ),
    ]
