# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-01 07:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webcore', '0003_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='photo',
            field=models.ImageField(null=True, upload_to='profile_photo'),
        ),
    ]
