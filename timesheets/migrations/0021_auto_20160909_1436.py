# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0020_auto_20160616_1443'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('initials', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=100, blank=True)),
                ('color', models.CharField(max_length=25, help_text='Color in CSS format (hexadecimal or rgb format)', default='#af0000')),
            ],
            options={
                'verbose_name_plural': 'tasks',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='timerecord',
            name='task',
            field=models.ForeignKey(null=True, to='timesheets.Task'),
            preserve_default=True,
        ),
    ]
