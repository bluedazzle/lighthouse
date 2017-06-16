# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Proxy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
                ('host', models.IPAddressField()),
                ('port', models.IntegerField(default=8080)),
                ('proxy_type', models.IntegerField(default=1, choices=[(1, 'HTTP'), (2, 'HTTPS')])),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
