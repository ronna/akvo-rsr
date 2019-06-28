# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-06-03 05:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rsr', '0153_auto_20190502_0522'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicatordimensionname',
            name='parent_dimension_name',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_dimension_names', to='rsr.IndicatorDimensionName', verbose_name='parent dimension name'),
        ),
        migrations.AddField(
            model_name='indicatordimensionvalue',
            name='parent_dimension_value',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_dimension_values', to='rsr.IndicatorDimensionValue', verbose_name='parent dimension value'),
        ),
    ]
