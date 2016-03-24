# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('date', models.DateField()),
                ('hours', models.FloatField()),
                ('employee', models.ForeignKey(to='timesheets.Employee')),
                ('project', models.ForeignKey(to='timesheets.SubProject')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='timeline',
            name='employee',
        ),
        migrations.RemoveField(
            model_name='timeline',
            name='project',
        ),
        migrations.DeleteModel(
            name='Timeline',
        ),
    ]
