# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-06-09 21:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0003_selectedgroup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selectedgroup',
            name='conversation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='selected_groups', to='bot.Conversation'),
        ),
    ]
