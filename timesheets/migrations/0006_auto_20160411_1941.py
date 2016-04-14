# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0005_subproject_finished'),
    ]

    operations = [
        migrations.AddField(
            model_name='subproject',
            name='analytic_code',
            field=models.CharField(max_length=30, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='employee',
            name='color',
            field=models.CharField(help_text='Color in CSS format (hexadecimal or rgb format)', default='#af0000', max_length=25),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='employee',
            name='user',
            field=models.OneToOneField(help_text='User binded to this employee', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
