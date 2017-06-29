# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from . import config
from .models import *


def refresh_all_beds():
    for bed in Bed.objects.all():
        refresh_bed_orders(bed)


def refresh_bed_orders(bed):
    today = datetime.now().date()

    orders = sorted(
        (lambda order: order.get_order_for_date().start_date),
        bed.orders
    )

    for order in orders:
        hist = order.get_order_for_date()
        if hist.status == Order.RESERVED:
            if hist.start_date == today:
                new_hist = order.create_new_history()
                new_hist.status = Order.AWAITING_ACTIVATION
                new_hist.save()
        elif hist.status == Order.AWAITING_ACTIVATION:
            if hist.start_date < today:
                new_hist = order.create_new_history()
                new_hist.status = Order.RESERVATION_CANCELLED
                new_hist.save()
        elif hist.status == Order.ACTIVE:
            if hist.end_date == today:
                new_hist = order.create_new_history()
                new_hist.status = Order.AWAITING_COMPLETION
                new_hist.save()
        elif hist.status == Order.AWAITING_COMPLETION:
            if hist.start_date < today:
                new_hist = order.create_new_history()
                new_hist.status = Order.COMPLETED
                new_hist.save()

    if bed.actual_order:
        hist = bed.actual_order.get_order_for_date()
        if hist.status in (Order.RESERVATION_CANCELLED, Order.COMPLETED):
            bed.actual_order = None

    if not bed.actual_order:
        for order in orders:
            if order.get_order_for_date().status == Order.AWAITING_ACTIVATION:
                bed.actual_order = order

    bed.save()


def cleanup_old_data():
    today = datetime.now().date()
    cleanup_date = today + timedelta(days=-config.DB_CLEANUP_THRESHOLD)

    Charge.objects.filter(date__lt=cleanup_date).delete()

    for order in Order.objects.all():
        if order.get_order_for_date().end_date < cleanup_date:
            order.delete()
