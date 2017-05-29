# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-29 19:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flocks', '0005_animalseparation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animalseparation',
            name='death',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='flocks.AnimalDeath'),
        ),
        migrations.AlterField(
            model_name='animalseparation',
            name='exit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='flocks.AnimalExits'),
        ),
    ]
