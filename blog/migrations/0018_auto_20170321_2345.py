# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-21 22:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_auto_20170321_2048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
