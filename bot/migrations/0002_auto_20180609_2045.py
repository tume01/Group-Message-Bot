# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-06-09 20:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='status',
            field=models.IntegerField(choices=[(1, 'inicio'), (2, 'elegir grupos'), (3, 'editando')], default=1),
        ),
    ]
