# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_project_is_closed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='parent',
            new_name='parent_project',
        ),
        migrations.AlterUniqueTogether(
            name='project',
            unique_together=set([('parent_project', 'initials')]),
        ),
        migrations.AlterIndexTogether(
            name='project',
            index_together=set([('parent_project', 'initials')]),
        ),
    ]
