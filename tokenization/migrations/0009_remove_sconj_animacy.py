# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-15 21:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tokenization', '0008_sconj_animacy'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sconj',
            name='animacy',
        ),
    ]