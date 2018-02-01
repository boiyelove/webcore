# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-03 23:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('webcore', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contacted_us',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contacted_us',
            name='name',
            field=models.CharField(default='me', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contacted_us',
            name='published_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contacted_us',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]