# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20161003_1527'),
        ('timesheets', '0028_auto_20161003_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='timerecord',
            name='project2',
            field=models.ForeignKey(null=True, to='projects.Project'),
            preserve_default=True,
        ),
    ]
