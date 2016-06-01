# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0014_project_finished'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=30)),
                ('description', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'permissions': (('view_category_list', 'Can view category list'),),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='subproject',
            name='category',
            field=models.ForeignKey(null=True, to='timesheets.Category', blank=True),
            preserve_default=True,
        ),
    ]
