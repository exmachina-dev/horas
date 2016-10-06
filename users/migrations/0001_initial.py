# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('initials', models.CharField(primary_key=True, serialize=False, max_length=5)),
                ('color', models.CharField(help_text='Color in CSS format (hexadecimal or rgb format)', default='#af0000', max_length=25)),
                ('is_active', models.BooleanField(help_text='Wether the employee is active in the company or not.', default=True)),
                ('production_ratio', models.FloatField()),
                ('user', models.OneToOneField(help_text='User binded to this employee', to=settings.AUTH_USER_MODEL, related_name='user_account')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
