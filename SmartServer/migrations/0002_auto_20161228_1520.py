# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-28 15:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SmartServer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devicesdbtable',
            name='deviceName',
        ),
        migrations.AddField(
            model_name='devicesdbtable',
            name='order',
            field=models.IntegerField(null=True),
        ),
    ]
