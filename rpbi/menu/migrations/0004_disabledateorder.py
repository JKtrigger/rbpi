# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-13 20:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_auto_20180106_2326'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisableDateOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disabled_date', models.DateField(verbose_name='Disabled date')),
            ],
        ),
    ]
