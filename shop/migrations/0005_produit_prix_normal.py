# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-11 23:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20180407_2255'),
    ]

    operations = [
        migrations.AddField(
            model_name='produit',
            name='prix_normal',
            field=models.FloatField(null=True, verbose_name='Prix normal du produit'),
        ),
    ]
