# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-04 11:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flocks', '0014_auto_20170604_1048'),
        ('buildings', '0007_auto_20170507_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='animalroomexit',
            name='farm_exit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='flocks.AnimalFarmExit'),
        ),
    ]
