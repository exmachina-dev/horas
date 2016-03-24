# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0003_auto_20160323_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='initials',
            field=models.CharField(unique=True, max_length=5),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='subproject',
            unique_together=set([('initials', 'parent_project')]),
        ),
        migrations.AlterUniqueTogether(
            name='timerecord',
            unique_together=set([('project', 'date', 'employee')]),
        ),
    ]
