# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-03 12:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0010_auto_20170802_1028'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='building',
            name='supplied_by',
        ),
        migrations.AddField(
            model_name='silo',
            name='building',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='buildings.Building'),
            preserve_default=False,
        ),
    ]