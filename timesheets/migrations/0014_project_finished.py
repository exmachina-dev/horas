# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0013_auto_20160511_1042'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='finished',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
