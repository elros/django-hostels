# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-04 19:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostels', '0008_orderhistory_taxhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderhistory',
            name='order_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='taxhistory',
            name='history_end',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='taxhistory',
            name='history_start',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='orderhistory',
            name='history_end',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='orderhistory',
            name='history_start',
            field=models.DateField(null=True),
        ),
    ]
