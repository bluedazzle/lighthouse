# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20170615_1428'),
    ]

    operations = [
        migrations.RenameField(
            model_name='proxy',
            old_name='proxy_type',
            new_name='protocol',
        ),
        migrations.AddField(
            model_name='proxy',
            name='available',
            field=models.BooleanField(default=True),
        ),
    ]
