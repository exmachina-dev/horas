# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_project_analytic_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='is_closed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
