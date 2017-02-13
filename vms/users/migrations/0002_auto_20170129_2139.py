# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-30 05:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='member_number',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]