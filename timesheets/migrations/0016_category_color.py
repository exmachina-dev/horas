# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0015_auto_20160601_0538'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='color',
            field=models.CharField(help_text='Color in CSS format (hexadecimal or rgb format)', default='#af0000', max_length=25),
            preserve_default=True,
        ),
    ]
