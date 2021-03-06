# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-17 16:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hostels', '0003_auto_20160517_1536'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bed',
            options={'verbose_name': 'Кровать', 'verbose_name_plural': 'Кровати'},
        ),
        migrations.AlterModelOptions(
            name='charge',
            options={'verbose_name': 'Платёж', 'verbose_name_plural': 'Платежи'},
        ),
        migrations.AlterModelOptions(
            name='hostel',
            options={'verbose_name': 'Хостел', 'verbose_name_plural': 'Хостелы'},
        ),
        migrations.AlterModelOptions(
            name='operator',
            options={'verbose_name': 'Оператор', 'verbose_name_plural': 'Операторы'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterModelOptions(
            name='tax',
            options={'verbose_name': 'Тариф', 'verbose_name_plural': 'Тарифы'},
        ),
        migrations.AlterModelOptions(
            name='taxgrade',
            options={'verbose_name': 'Порог тарифа', 'verbose_name_plural': 'Пороги тарифа'},
        ),
        migrations.AlterField(
            model_name='bed',
            name='actual_order',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hostels.Order', verbose_name='Текущий заказ'),
        ),
        migrations.AlterField(
            model_name='bed',
            name='gender',
            field=models.IntegerField(choices=[(0, 'Муж'), (1, 'Жен')], verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='bed',
            name='hostel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hostels.Hostel', verbose_name='Хостел'),
        ),
        migrations.AlterField(
            model_name='bed',
            name='tax',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hostels.Tax', verbose_name='Тариф'),
        ),
        migrations.AlterField(
            model_name='charge',
            name='date',
            field=models.DateTimeField(verbose_name='Дата формирования'),
        ),
        migrations.AlterField(
            model_name='charge',
            name='is_income',
            field=models.BooleanField(verbose_name='Доход'),
        ),
        migrations.AlterField(
            model_name='charge',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hostels.Order', verbose_name='Заказ'),
        ),
        migrations.AlterField(
            model_name='charge',
            name='reason',
            field=models.IntegerField(choices=[(0, 'Причина 0'), (1, 'Причина 1')], verbose_name='Причина'),
        ),
        migrations.AlterField(
            model_name='charge',
            name='value',
            field=models.FloatField(default=0.0, verbose_name='Сумма'),
        ),
        migrations.AlterField(
            model_name='hostel',
            name='address',
            field=models.CharField(max_length=100, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='hostel',
            name='city',
            field=models.CharField(max_length=50, verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='hostel',
            name='tax',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hostels.Tax', verbose_name='Тариф'),
        ),
        migrations.AlterField(
            model_name='operator',
            name='full_name',
            field=models.CharField(max_length=50, verbose_name='ФИО'),
        ),
        migrations.AlterField(
            model_name='operator',
            name='hostels',
            field=models.ManyToManyField(blank=True, to='hostels.Hostel', verbose_name='Хостелы'),
        ),
        migrations.AlterField(
            model_name='operator',
            name='identification',
            field=models.CharField(max_length=150, verbose_name='Паспортные данные'),
        ),
        migrations.AlterField(
            model_name='operator',
            name='is_admin',
            field=models.BooleanField(default=False, verbose_name='Администратор'),
        ),
        migrations.AlterField(
            model_name='operator',
            name='phone_number',
            field=models.CharField(max_length=50, verbose_name='Номер телефона'),
        ),
        migrations.AlterField(
            model_name='operator',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='order',
            name='end_date',
            field=models.DateField(verbose_name='Дата выезда'),
        ),
        migrations.AlterField(
            model_name='order',
            name='guest_full_name',
            field=models.CharField(max_length=100, verbose_name='ФИО клиента'),
        ),
        migrations.AlterField(
            model_name='order',
            name='guest_identification',
            field=models.CharField(max_length=150, verbose_name='Паспортные данные клиента'),
        ),
        migrations.AlterField(
            model_name='order',
            name='guest_phone_number',
            field=models.CharField(max_length=50, verbose_name='Телефоны клиента'),
        ),
        migrations.AlterField(
            model_name='order',
            name='start_date',
            field=models.DateField(verbose_name='Дата въезда'),
        ),
        migrations.AlterField(
            model_name='order',
            name='value',
            field=models.FloatField(default=0.0, verbose_name='Сумма'),
        ),
    ]
