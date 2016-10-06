# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('projects', '0001_initial')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('initials', models.CharField(max_length=30)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('parent', models.ForeignKey(default=None, blank=True, to='projects.Project', null=True, on_delete=django.db.models.deletion.SET_DEFAULT)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
