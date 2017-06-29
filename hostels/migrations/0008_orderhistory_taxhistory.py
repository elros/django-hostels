# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-04 19:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hostels', '0007_auto_20160523_1918'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(verbose_name='Дата въезда')),
                ('end_date', models.DateField(verbose_name='Дата выезда')),
                ('value', models.FloatField(default=0.0, verbose_name='Сумма')),
                ('guest_full_name', models.CharField(max_length=100, verbose_name='ФИО клиента')),
                ('guest_identification', models.CharField(max_length=150, verbose_name='Паспортные данные клиента')),
                ('guest_phone_number', models.CharField(max_length=50, verbose_name='Телефоны клиента')),
                ('history_start', models.DateField()),
                ('history_end', models.DateField()),
                ('bed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hostels.Bed', verbose_name='Кровать')),
            ],
        ),
        migrations.CreateModel(
            name='TaxHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tax_name', models.CharField(max_length=200)),
                ('tax_grades', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hostels.TaxGrade')),
            ],
        ),
    ]
