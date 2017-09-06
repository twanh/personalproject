# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-06 15:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('desc', models.TextField(blank=True)),
                ('image_url', models.URLField(blank=True, null=True, verbose_name='Image URL')),
                ('original_price', models.CharField(blank=True, max_length=15)),
                ('g2a_price', models.CharField(blank=True, max_length=15)),
                ('g2a_url', models.URLField(blank=True, null=True, verbose_name='G2a URL')),
                ('kinguin_price', models.CharField(blank=True, max_length=15)),
                ('kinguin_url', models.URLField(blank=True, null=True, verbose_name='Kinguin URL')),
                ('greenman_price', models.CharField(blank=True, max_length=15)),
                ('greenman_url', models.URLField(blank=True, null=True, verbose_name='Greenman URL')),
                ('gamestop_price', models.CharField(blank=True, max_length=15)),
                ('gamestop_url', models.URLField(blank=True, null=True, verbose_name='Gamestop URL')),
                ('images', models.TextField(blank=True, default='[]')),
                ('rating', models.IntegerField(blank=True, null=True)),
                ('community_reddit', models.URLField(blank=True, null=True, verbose_name='Reddit community urls')),
            ],
        ),
    ]
