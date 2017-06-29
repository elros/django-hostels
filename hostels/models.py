# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied


class Hostel(models.Model):
    city = models.CharField(max_length=50, verbose_name='Город')
    address = models.CharField(max_length=100, verbose_name='Адрес')
    tax = models.ForeignKey('Tax', on_delete=models.CASCADE, verbose_name='Тариф')
    phone_number = models.CharField(max_length=50, verbose_name='Номер телефона')

    def orders(self):
        result = []
        for bed in self.bed_set.all():
            result += bed.order_set.all()
        return result

    def charges(self):
        result = []
        for order in self.orders():
            result += order.charge_set.all()
        return result

    def beds_count(self):
        return self.bed_set.count()

    def free_beds_count(self):
        return len([bed for bed in self.bed_set.all() if bed.actual_order is None])

    def nonfree_beds_count(self):
        return self.bed_set.count() - self.free_beds_count()

    def today_value_income(self):
        today = datetime.now().date()
        return self.period_value_income(start_date=today, end_date=today)

    def today_value_outgo(self):
        today = datetime.now().date()
        return self.period_value_outgo(start_date=today, end_date=today)

    def period_value_income(self, start_date, end_date):
        result = 0.0
        for charge in self.charges():
            if charge.is_income and (start_date <= charge.date.date() <= end_date):
                result += charge.value
        return result

    def period_value_outgo(self, start_date, end_date):
        result = 0.0
        for charge in self.charges():
            if not charge.is_income and (start_date <= charge.date.date() <= end_date):
                result += charge.value
        return result

    def today_settlements(self):
        today = datetime.now().date()
        return self.period_settlements(start_date=today, end_date=today)

    def today_departures(self):
        today = datetime.now().date()
        return self.period_departures(start_date=today, end_date=today)

    def period_settlements(self, start_date, end_date):
        return len(list(filter(
            (lambda charge:
                start_date <= charge.date.date() <= end_date
                and charge.reason == Charge.ORDER_ACTIVATION
            ),
            self.charges()
        )))

    def period_departures(self, start_date, end_date):
        return len(list(filter(
            (lambda order:
                start_date <= order.end_date <= end_date
                and order.status == Order.COMPLETED
            ),
            self.orders()
        )))

    def __str__(self):
        return '%s, %s' % (self.city, self.address)

    class Meta:
        verbose_name = 'Хостел'
        verbose_name_plural = 'Хостелы'


class Operator(models.Model):
    user = models.OneToOneField(User, verbose_name='Пользователь')
    full_name = models.CharField(max_length=50, verbose_name='ФИО')
    identification = models.CharField(max_length=150, verbose_name='Паспортные данные')
    phone_number = models.CharField(max_length=50, verbose_name='Номер телефона')
    hostels = models.ManyToManyField(Hostel, blank=True, verbose_name='Хостелы')
    is_admin = models.BooleanField(default=False, verbose_name='Администратор')

    def __str__(self):
        return '%s' % (self.full_name)

    class Meta:
        verbose_name = 'Оператор'
        verbose_name_plural = 'Операторы'

    def get_bed_list(self):
        return Bed.objects.filter(hostel__in=self.hostels.all())

    def get_bed(self, bed_id):
        bed = get_object_or_404(Bed, pk=bed_id)
        if bed in self.get_bed_list():
            return bed
        else:
            raise PermissionDenied

    def get_order_list(self):
        orders = []
        for bed in self.get_bed_list():
            orders += bed.order_set.all()
        return orders

    def get_order(self, order_id):
        order = get_object_or_404(Order, pk=order_id)
        if order in self.get_order_list():
            return order
        else:
            raise PermissionDenied


class Bed(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, verbose_name='Хостел')
    tax = models.ForeignKey('Tax', on_delete=models.CASCADE, verbose_name='Тариф')
    actual_order = models.OneToOneField(
        'Order',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='actual_bed',
        verbose_name='Текущий заказ'
    )

    MALE = 0
    FEMALE = 1
    Gender = (
        (MALE  , 'Муж'),
        (FEMALE, 'Жен'),
    )
    gender = models.IntegerField(choices=Gender, verbose_name='Пол')

    def gender_text(self):
        return Bed.Gender[self.gender][1]

    def __str__(self):
        return 'Кровать #%d (%s)' % (self.id, self.hostel)

    class Meta:
        verbose_name = 'Кровать'
        verbose_name_plural = 'Кровати'

    def get_tax_value(self, days=None, start_date=None, end_date=None):
        if days is None:
            days = (end_date - start_date).days

        # Для неправильных периодов ставим минимальную цену.
        if days < 0:
            days = 1

        # Особенность формулы количества дней. Не должно дублироваться в других местах системы.
        # Если человек заехал на день, то считаем цену как один день, а не ноль дней. 
        if (start_date is not None and start_date == end_date) or (days == 0):
            days = 1

        for grade in self.tax.sorted_grades(reverse=True):
            if days >= grade.threshold_days:
                return days * grade.day_price
        else:
            return 0

    def has_orders_for_date(self, date):
        for order in self.order_set.all():
            if order.start_date <= date <= order.end_date:
                return True
        else:
            return False

    def get_order_for_date(self, date):
        for order in self.order_set.all():
            if order.start_date <= date <= order.end_date:
                return order
        else:
            return None


class Charge(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, verbose_name='Заказ')
    value = models.FloatField(default=0.0, verbose_name='Сумма')
    is_income = models.BooleanField(verbose_name='Доход')
    date = models.DateTimeField(verbose_name='Дата формирования')

    ORDER_ACTIVATION = 0
    END_DATE_CHANGE = 1
    Reason = (
        (ORDER_ACTIVATION, 'Заселение'),
        (END_DATE_CHANGE , 'Изменение сроков проживания'),
    )
    reason = models.IntegerField(choices=Reason, verbose_name='Причина')

    def reason_text(self):
        return Charge.Reason[self.reason][1]

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'


class Order(models.Model):
    bed = models.ForeignKey(Bed, verbose_name='Кровать')
    start_date = models.DateField(verbose_name='Дата въезда')
    end_date = models.DateField(verbose_name='Дата выезда')
    value = models.FloatField(default=0.0, verbose_name='Сумма')
    guest_full_name = models.CharField(max_length=100, verbose_name='ФИО клиента')
    guest_identification = models.CharField(max_length=150, verbose_name='Паспортные данные клиента')
    guest_phone_number = models.CharField(max_length=50, verbose_name='Телефоны клиента')

    RESERVED = 1
    AWAITING_ACTIVATION = 2
    RESERVATION_CANCELLED = 3
    ACTIVE = 4
    AWAITING_COMPLETION = 5
    COMPLETED = 6
    Status = (
        (RESERVED             , 'Забронирован'               ),
        (AWAITING_ACTIVATION  , 'Ожидает подтверждения брони'),
        (RESERVATION_CANCELLED, 'Бронирование отменено'      ),
        (ACTIVE               , 'Активен'                    ),
        (AWAITING_COMPLETION  , 'Готов к завершению'         ),
        (COMPLETED            , 'Успешно завершён'           ),
    )
    status = models.IntegerField(choices=Status, verbose_name='Статус')

    def status_text(self):
        return Order.Status[self.status - 1][1]

    def hostel(self):
        return self.bed.hostel
    hostel.short_description = 'Хостел'

    def __str__(self):
        return 'Заказ #%d' % (self.id)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def check_dates(self):
        fail = False

        if self.start_date > self.end_date:
            fail = True

        for other in self.bed.order_set.all():
            if self == other:
                continue
            is_before = (self.start_date <= other.start_date and self.end_date <= other.start_date)
            is_after = (self.start_date >= other.end_date and self.end_date >= other.end_date)
            if not (is_before or is_after):
                fail = True
        
        return not fail


class Tax(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'

    def sorted_grades(self, reverse=False):
        return sorted(
            self.taxgrade_set.all(),
            key=(lambda grade: grade.threshold_days),
            reverse=reverse,
        )


class TaxGrade(models.Model):
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE)
    threshold_days = models.IntegerField()
    day_price = models.FloatField()

    def __str__(self):
        return 'Порог %d дней, тариф %s' % (self.threshold_days, self.tax.name)

    class Meta:
        verbose_name = 'Порог тарифа'
        verbose_name_plural = 'Пороги тарифа'


class OrderHistory(models.Model):
    order_id = models.IntegerField(default=0)
    bed = models.ForeignKey(Bed, verbose_name='Кровать')
    start_date = models.DateField(verbose_name='Дата въезда')
    end_date = models.DateField(verbose_name='Дата выезда')
    value = models.FloatField(default=0.0, verbose_name='Сумма')
    guest_full_name = models.CharField(max_length=100, verbose_name='ФИО клиента')
    guest_identification = models.CharField(max_length=150, verbose_name='Паспортные данные клиента')
    guest_phone_number = models.CharField(max_length=50, verbose_name='Телефоны клиента')
    history_start = models.DateTimeField(null=True)
    history_end = models.DateTimeField(null=True)

class TaxHistory(models.Model):
    tax_name = models.CharField(max_length=200)
    tax_grades = models.ManyToManyField(TaxGrade)
    history_start = models.DateTimeField(null=True)
    history_end = models.DateTimeField(null=True)