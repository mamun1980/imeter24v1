# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-28 11:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MeterRead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meterread', models.CharField(max_length=64)),
            ],
            options={
                'ordering': ['meterread'],
                'db_table': 'meterreads_dummy',
                'verbose_name': 'Meter Reads Dummy',
                'verbose_name_plural': 'Meter Reads Dummy',
            },
        ),
    ]
