# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-02 11:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0035_auto_20170402_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='textc',
            field=models.TextField(max_length=200, null=True),
        ),
    ]