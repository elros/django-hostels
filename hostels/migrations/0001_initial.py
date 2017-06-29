# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-17 15:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.IntegerField(choices=[(0, 'Муж'), (1, 'Жен')])),
            ],
        ),
        migrations.CreateModel(
            name='Charge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(default=0.0)),
                ('is_income', models.BooleanField()),
                ('date', models.DateTimeField()),
                ('reason', models.IntegerField(choices=[(0, 'Причина 0'), (1, 'Причина 1')])),
            ],
        ),
        migrations.CreateModel(
            name='Hostel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('identification', models.CharField(max_length=150)),
                ('phone_number', models.CharField(max_length=50)),
                ('is_admin', models.BooleanField(default=False)),
                ('hostels', models.ManyToManyField(to='hostels.Hostel')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('value', models.FloatField(default=0.0)),
                ('guest_full_name', models.CharField(max_length=100)),
                ('guest_identification', models.CharField(max_length=150)),
                ('guest_phone_number', models.CharField(max_length=50)),
                ('status', models.IntegerField(choices=[(1, 'Забронирован'), (2, 'Ожидает подтверждения брони'), (3, 'Бронирование отменено'), (4, 'Активен'), (5, 'Готов к завершению'), (6, 'Успешно завершён')])),
            ],
        ),
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='TaxGrade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('threshold_days', models.IntegerField()),
                ('day_price', models.FloatField()),
                ('tax', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hostels.Tax')),
            ],
        ),
        migrations.AddField(
            model_name='hostel',
            name='tax',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hostels.Tax'),
        ),
        migrations.AddField(
            model_name='charge',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hostels.Order'),
        ),
        migrations.AddField(
            model_name='bed',
            name='actual_order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hostels.Order'),
        ),
        migrations.AddField(
            model_name='bed',
            name='hostel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hostels.Hostel'),
        ),
        migrations.AddField(
            model_name='bed',
            name='tax',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hostels.Tax'),
        ),
    ]