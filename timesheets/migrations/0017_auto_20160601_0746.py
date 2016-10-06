# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0016_category_color'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'permissions': (('view_category_list', 'Can view category list'),), 'verbose_name_plural': 'categories'},
        ),
        migrations.AlterModelOptions(
            name='subproject',
            options={'ordering': ('full_initials',), 'permissions': (('view_subproject_list', 'Can view subproject list'),)},
        ),
        migrations.AddField(
            model_name='subproject',
            name='full_initials',
            field=models.CharField(editable=False, max_length=50, null=True),
            preserve_default=True,
        ),
    ]
