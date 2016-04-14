# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0004_auto_20160324_0920'),
    ]

    operations = [
        migrations.AddField(
            model_name='subproject',
            name='finished',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
