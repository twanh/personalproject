# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-21 11:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.CharField(max_length=50)),
                ('seller', models.CharField(choices=[('g2a', 'G2a'), ('king', 'Kinguin'), ('gamestop', 'Gamestop')], max_length=50)),
                ('original_price', models.CharField(max_length=4)),
                ('current_price', models.CharField(max_length=4)),
                ('header_img', models.URLField()),
                ('desc', models.TextField()),
            ],
        ),
    ]
