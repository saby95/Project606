# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-20 05:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_researchtasks_worker_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='researchtasks',
            name='worker_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]