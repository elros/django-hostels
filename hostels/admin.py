# -*- conding: utf-8 -*-
from django.contrib import admin

from .models import Hostel, Operator, Bed, Charge, Order, Tax, TaxGrade, OrderHistory, TaxHistory


class OperatorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'is_admin')

admin.site.register(Operator, OperatorAdmin)


class BedInline(admin.TabularInline):
    model = Bed
    extra = 2

class HostelAdmin(admin.ModelAdmin):
    list_display = ('city', 'address', 'tax', 'beds_count')
    # Свободных кроватей
    # Занятых
    # Доход/расход за день
    # Число въездов/отъездов за день
    list_filter = ('city',)
    inlines = [BedInline]

admin.site.register(Hostel, HostelAdmin)


class ChargeAdmin(admin.ModelAdmin):
    list_display = ('date', 'order', 'value', 'is_income')
    list_filter = ('date', 'is_income')

admin.site.register(Charge, ChargeAdmin)


class TaxGradeInline(admin.TabularInline):
    model = TaxGrade
    extra = 2

class TaxAdmin(admin.ModelAdmin):
    inlines = [TaxGradeInline]

admin.site.register(Tax, TaxAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'status', 'guest_full_name', 'value', 'hostel')
    list_filter = ('start_date', 'end_date')
    fieldsets = (
        ('Общие данные', {
            'fields': ('status', 'value', 'bed')
        }),
        ('Даты заказа', {
            'fields': ('start_date', 'end_date'),
        }),
        ('Данные о клиенте', {
            'fields': ('guest_full_name', 'guest_identification', 'guest_phone_number')
        }),
    )
    # inlines = [BedInline]

admin.site.register(Order, OrderAdmin)

admin.site.register(OrderHistory)
admin.site.register(TaxHistory)