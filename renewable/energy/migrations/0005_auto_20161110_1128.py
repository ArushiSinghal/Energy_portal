# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2016-11-10 05:58
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('energy', '0004_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadidea',
            name='likes',
            field=models.ManyToManyField(related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='uploadidea',
            name='slug',
            field=models.SlugField(default=datetime.datetime(2016, 11, 10, 5, 58, 37, 160461, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
