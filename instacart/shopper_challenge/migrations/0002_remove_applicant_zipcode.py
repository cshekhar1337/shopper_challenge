# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-17 20:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopper_challenge', '0001_mymodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicant',
            name='zipcode',
        ),
    ]
