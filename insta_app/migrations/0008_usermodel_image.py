# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-12 19:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insta_app', '0007_auto_20171111_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='image',
            field=models.FileField(default=dir, upload_to='profile_images'),
            preserve_default=False,
        ),
    ]
