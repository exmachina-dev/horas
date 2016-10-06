# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('initials', models.CharField(max_length=30)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('parent', models.ForeignKey(blank=True, to='projects.Project', null=True, default=None, on_delete=django.db.models.deletion.SET_DEFAULT)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
