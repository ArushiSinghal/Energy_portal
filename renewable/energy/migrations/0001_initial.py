# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2016-11-08 15:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Googlenews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=512)),
                ('original_url', models.CharField(max_length=1024)),
                ('pubdate', models.DateTimeField()),
                ('imageurl', models.CharField(max_length=512, null=True)),
                ('description', models.TextField()),
                ('pub_agency', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='Querynews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField(max_length=300)),
                ('num', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UploadIdea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(max_length=800)),
                ('upload_image', models.FileField(null=True, upload_to='uploads/')),
                ('date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('idea', models.TextField(max_length=3000)),
                ('link', models.CharField(max_length=600, null=True)),
                ('uploader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
