# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-28 06:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0010_auto_20181028_0621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audit',
            name='task_correct',
            field=models.BooleanField(default=None),
        ),
    ]
