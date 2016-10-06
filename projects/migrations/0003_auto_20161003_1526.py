# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20161003_1514'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='project',
            index_together=set([('parent', 'initials')]),
        ),
    ]
