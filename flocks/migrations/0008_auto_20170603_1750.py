# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-03 17:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flocks', '0007_auto_20170603_1749'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='animalexits',
            name='mixed_exit',
        ),
        migrations.DeleteModel(
            name='MixedFlockAnimalExit',
        ),
    ]
