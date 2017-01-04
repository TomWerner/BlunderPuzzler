# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-04 17:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Puzzle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=50)),
                ('severity', models.CharField(choices=[(1, 'Inaccuracy'), (2, 'Mistake'), (3, 'Blunder')], max_length=1)),
            ],
        ),
    ]