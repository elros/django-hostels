# -*- conding: utf-8 -*-
from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.models import User

from .forms import LoginForm, ActualOrderForm, ChangeOrderEndDateForm, ReservationForm, \
                   ConfirmCompletionForm, ActivateReservationForm, CancelReservationForm, \
                   RemoveReservationForm, EditReservationDatesForm
from .models import Hostel, Operator, Bed, Charge, Order, Tax, TaxGrade, OrderHistory, TaxHistory
from .config import ERROR_MESSAGES, RESERVATION_CALENDAR_DAYS
from . import utils


class Login(View):

    def get(self, request):
        if not request.user.is_authenticated():
            form = LoginForm()
            return render(request, 'hostels/login.html', {'form': form})
        else:
            return redirect(reverse('hostels:index'))

    def post(self, request):
        form = LoginForm(request.POST)
        error = None
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if 'next' in request.GET:
                    return redirect(request.GET['next'])
                else:
                    return redirect(reverse('hostels:index'))
            else:
                error = ERROR_MESSAGES['bad_input']
        return render(
            request,
            'hostels/login.html',
            {
                'form': form,
                'error': error,
            }
        )


class Logout(View):

    def get(self, request):
        logout(request)
        return redirect(reverse('hostels:login'))


class IndexView(LoginRequiredMixin, View):

    def get(self, request):
        if request.user.operator.is_admin:
            return redirect(reverse('hostels:manage_index'))
        else:
            return redirect(reverse('hostels:bed_list'))


##########################
###                    ###
###   Operator views   ###
###                    ###
##########################



class OperatorView(LoginRequiredMixin, View):

    pass


class BedListView(OperatorView):

    def get(self, request):
        return render(
            request,
            'hostels/bed_list.html',
            {
                'bed_list': sorted(
                    request.user.operator.get_bed_list(),
                    key=(lambda bed: bed.id),
                )
            }
        )


class OrderListView(OperatorView):

    def get(self, request):
        return render(
            request,
            'hostels/order_list.html',
            {
                'order_list': sorted(
                    request.user.operator.get_order_list(),
                    key=(lambda order: order.id),
                    reverse=True,
                )
            }
        )


class HostelListView(OperatorView):

    def get(self, request):
        hostels = Hostel.objects.all()
        cities = {}
        for hostel in hostels:
            cities[hostel.city] = cities.get(hostel.city, []) + [hostel]
        hostel_list = [
            (city, cities[city])
            for city in sorted(cities.keys())
        ]
        return render(
            request,
            'hostels/hostel_list.html',
            {
                'hostel_list': hostel_list,
            }
        )


class CreateActualOrderView(OperatorView):

    def get(self, request, bed_id):
        bed = self.request.user.operator.get_bed(bed_id)
        today = datetime.now().date()
        form = ActualOrderForm(initial={'start_date': today})
        return render(
            request,
            'hostels/create_actual_order.html',
            {
                'form': form,
                'bed': bed,
            }
        )

    def post(self, request, bed_id):
        bed = self.request.user.operator.get_bed(bed_id)
        form = ActualOrderForm(request.POST)
        error = None
        if form.is_valid():
            order = Order(
                bed=bed,
                start_date=form.cleaned_data['start_date'],
                end_date=form.cleaned_data['end_date'],
                value=bed.get_tax_value(
                    start_date=form.cleaned_data['start_date'],
                    end_date=form.cleaned_data['end_date'],
                ),
                guest_full_name=form.cleaned_data['guest_full_name'],
                guest_identification=form.cleaned_data['guest_identification'],
                guest_phone_number=form.cleaned_data['guest_phone_number'],
                status=Order.ACTIVE,
            )
            if not order.check_dates():
                error = ERROR_MESSAGES['bad_date']
            else:
                order.save()
                bed.actual_order = order
                bed.save()
                Charge(
                    order=order,
                    value=order.value,
                    is_income=True,
                    date=datetime.now(),
                    reason=Charge.ORDER_ACTIVATION,
                ).save()
                return redirect(reverse('hostels:bed_list'))
        return render(
            request,
            'hostels/create_actual_order.html',
            {
                'form': form,
                'error': error,
                'bed': bed,
            }
        )


class ChangeOrderEndDateView(OperatorView):

    def get(self, request, bed_id):
        bed = self.request.user.operator.get_bed(bed_id)
        form = ChangeOrderEndDateForm(
            initial={
                'start_date': bed.actual_order.start_date,
                'end_date': bed.actual_order.end_date,
                'old_value': bed.actual_order.value,
            }
        )
        return render(
            request,
            'hostels/change_order_end_date.html',
            {
                'form': form,
                'bed': bed,
            }
        )

    def post(self, request, bed_id):
        bed = self.request.user.operator.get_bed(bed_id)
        form = ChangeOrderEndDateForm(request.POST)
        error = None
        if form.is_valid():
            order = bed.actual_order
            order.end_date = form.cleaned_data['end_date']
            previous_value = order.value
            order.value = bed.get_tax_value(
                start_date=order.start_date,
                end_date=order.end_date,
            )
            if not order.check_dates():
                error = ERROR_MESSAGES['bad_date']
            else:
                order.save()
                Charge(
                    order=order,
                    value=abs(order.value - previous_value),
                    is_income=(order.value > previous_value),
                    date=datetime.now(),
                    reason=Charge.END_DATE_CHANGE,
                ).save()
                return redirect(reverse('hostels:bed_list'))
        return render(
            request,
            'hostels/change_order_end_date.html',
            {
                'form': form,
                'error': error,
                'bed': bed,
            }
        )


class CreateReservationView(OperatorView):

    def get(self, request, bed_id):
        bed = self.request.user.operator.get_bed(bed_id)
        form = ReservationForm(initial={
            'start_date': request.GET.get('start_date'),
        })
        return render(
            request,
            'hostels/create_reservation.html',
            {
                'form': form,
                'bed': bed,
            }
        )

    def post(self, request, bed_id):
        bed = self.request.user.operator.get_bed(bed_id)
        form = ReservationForm(request.POST)
        error = None
        if form.is_valid():
            order = Order(
                bed=bed,
                start_date=form.cleaned_data['start_date'],
                end_date=form.cleaned_data['end_date'],
                value=bed.get_tax_value(
                    start_date=form.cleaned_data['start_date'],
                    end_date=form.cleaned_data['end_date'],
                ),
                guest_full_name=form.cleaned_data['guest_full_name'],
                guest_identification=form.cleaned_data['guest_identification'],
                guest_phone_number=form.cleaned_data['guest_phone_number'],
                status=Order.RESERVED,
            )
            if not order.check_dates():
                error = ERROR_MESSAGES['bad_date']
            else:
                order.save()
                return redirect(reverse('hostels:bed_list'))
        return render(
            request,
            'hostels/create_reservation.html',
            {
                'form': form,
                'error': error,
                'bed': bed,
            }
        )


class ReservationCalendarView(OperatorView):

    def get(self, request):
        now = datetime.now()
        days = [(now + timedelta(days=k)).date() for k in range(RESERVATION_CALENDAR_DAYS)]
        beds = request.user.operator.get_bed_list()
        calendar = [
            (
                day,
                [
                    [
                        bed,
                        bed.get_order_for_date(day),
                    ] for bed in beds
                ]
            ) for day in days
        ]

        search = request.GET.get('search', '').lower()
        if search:
            for day, _beds in calendar:
                for item in _beds:
                    bed, order = item[0], item[1]
                    if order and search in order.guest_full_name.lower():
                        item.append(True)

        return render(
            request,
            'hostels/reservation_calendar.html',
            {
                'beds': beds,
                'days': days,
                'calendar': calendar,
            }
        )



class ConfirmCompletionView(OperatorView):

    def get(self, request, bed_id):
        bed = self.request.user.operator.get_bed(bed_id)
        order = bed.actual_order
        form = ConfirmCompletionForm(initial={
            'start_date': order.start_date,
            'end_date': order.end_date,
            'guest_full_name': order.guest_full_name,
            'guest_identification': order.guest_identification,
            'guest_phone_number': order.guest_phone_number,
            'value': order.value,
        })
        return render(
            request,
            'hostels/confirm_completion.html',
            {
                'form': form,
                'bed': bed,
            }
        )

    def post(self, request, bed_id):
        bed = self.request.user.operator.get_bed(bed_id)
        order = bed.actual_order
        order.status = Order.COMPLETED
        order.save()
        bed.actual_order = None
        bed.save()
        return redirect(reverse('hostels:bed_list'))


class ActivateReservationView(OperatorView):

    def get(self, request, bed_id):
        bed = self.request.user.operator.get_bed(bed_id)
        order = bed.actual_order
        form = ActivateReservationForm(initial={
            'start_date': order.start_date,
            'end_date': order.end_date,
            'guest_full_name': order.guest_full_name,
            'guest_identification': order.guest_identification,
            'guest_phone_number': order.guest_phone_number,
            'value': order.value,
        })
        return render(
            request,
            'hostels/activate_reservation.html',
            {
                'form': form,
                'bed': bed,
            }
        )

    def post(self, request, bed_id):
        bed = self.request.user.operator.get_bed(bed_id)
        order = bed.actual_order
        order.status = Order.ACTIVE
        order.save()
        Charge(
            order=order,
            value=order.value,
            is_income=True,
            date=datetime.now(),
            reason=Charge.ORDER_ACTIVATION,
        ).save()
        return redirect(reverse('hostels:bed_list'))


class CancelReservationView(OperatorView):

    def get(self, request, bed_id):
        bed = self.request.user.operator.get_bed(bed_id)
        order = bed.actual_order
        form = CancelReservationForm(initial={
            'start_date': order.start_date,
            'end_date': order.end_date,
            'guest_full_name': order.guest_full_name,
            'guest_identification': order.guest_identification,
            'guest_phone_number': order.guest_phone_number,
            'value': order.value,
        })
        return render(
            request,
            'hostels/cancel_reservation.html',
            {
                'form': form,
                'bed': bed,
            }
        )

    def post(self, request, bed_id):
        bed = self.request.user.operator.get_bed(bed_id)
        order = bed.actual_order
        order.status = Order.RESERVATION_CANCELLED
        order.save()
        bed.actual_order = None
        bed.save()
        return redirect(reverse('hostels:bed_list'))


class RemoveReservationView(OperatorView):

    def get(self, request, order_id):
        order = request.user.operator.get_order(order_id)
        form = RemoveReservationForm(initial={
            'status': order.status_text(),
            'start_date': order.start_date,
            'end_date': order.end_date,
            'guest_full_name': order.guest_full_name,
            'guest_identification': order.guest_identification,
            'guest_phone_number': order.guest_phone_number,
            'value': order.value,
        })
        return render(
            request,
            'hostels/remove_reservation.html',
            {
                'form': form,
            }
        )

    def post(self, request, order_id):
        order = request.user.operator.get_order(order_id)
        if order.status not in (Order.RESERVED, Order.AWAITING_ACTIVATION):
            return HttpResponseBadRequest()
        else:
            order.status = Order.RESERVATION_CANCELLED
            order.save()
            return redirect(reverse('hostels:bed_list'))


class BedTaxValueView(OperatorView):

    def get(self, request, bed_id):
        if 'days' not in request.GET:
            return HttpResponseBadRequest()
        else:
            days = int(request.GET['days'])

        bed = request.user.operator.get_bed(bed_id)
        tax_value = bed.get_tax_value(days=days)
        return HttpResponse(tax_value)


class TaxesView(OperatorView):

    def get(self, request):
        beds = request.user.operator.get_bed_list()
        taxes = set([bed.tax for bed in beds])
        return render(
            request,
            'hostels/tax_list.html',
            {
                'taxes': taxes,
            }
        )


class ChangeReservationDatesView(OperatorView):

    def get(self, request, order_id):
        order = request.user.operator.get_order(order_id)
        form = EditReservationDatesForm(initial={
            'status': order.status_text(),
            'start_date': order.start_date,
            'end_date': order.end_date,
            'guest_full_name': order.guest_full_name,
            'guest_identification': order.guest_identification,
            'guest_phone_number': order.guest_phone_number,
            'value': order.value,
        })
        return render(
            request,
            'hostels/change_reservation_dates.html',
            {
                'form': form,
                'bed': order.bed,
            }
        )

    def post(self, request, order_id):
        order = request.user.operator.get_order(order_id)
        form = EditReservationDatesForm(request.POST)
        error = None
        if form.is_valid():
            order.start_date = form.cleaned_data['start_date']
            order.end_date = form.cleaned_data['end_date']
            order.value = order.bed.get_tax_value(
                start_date=form.cleaned_data['start_date'],
                end_date=form.cleaned_data['end_date'],
            )
            if not order.check_dates():
                error = ERROR_MESSAGES['bad_date']
            else:
                order.save()
                return redirect(reverse('hostels:bed_list'))
        return render(
            request,
            'hostels/change_reservation_dates.html',
            {
                'form': form,
                'error': error,
                'bed': order.bed,
            }
        )


#########################
###                   ### 
###   Manager views   ###
###                   ###
#########################


class AdminRequiredMixin(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.operator.is_admin


class AdminView(LoginRequiredMixin, AdminRequiredMixin, View): pass


class ManageIndexView(AdminView):

    def get(self, request):
        return redirect(reverse('hostels:manage_hostels'))


class ManageHostelsView(AdminView):

    def get(self, request):
        hostels = Hostel.objects.all()
        if 'operator_id' in request.GET:
            operator = Operator.objects.get(pk=int(request.GET['operator_id']))
            hostels = filter(
                (lambda hostel: operator in hostel.operator_set.all()),
                hostels
            )

        return render(
            request,
            'hostels/manage_hostels.html',
            {
                'hostels': hostels,
                'options': {
                    'tax': [(tax.id, tax.name) for tax in Tax.objects.all()],
                    'operators': [(op, str(op)) for op in Operator.objects.all()],
                },
                'operators': Operator.objects.order_by('id'),
            }
        )

    def post(self, request):
        hostel = Hostel(
            city=request.POST['city'],
            address=request.POST['address'],
            tax=Tax.objects.get(pk=int(request.POST['tax_id'])),
            phone_number=request.POST['phone_number'],
        )
        hostel.save()

        for username in request.POST.getlist('operators'):
            operator = Operator.objects.filter(user__username=username).first()
            hostel.operator_set.add(operator)
        hostel.save()

        return redirect(request.get_full_path())


class ManageEditHostelView(AdminView):

    def post(self, request, id):
        hostel = Hostel.objects.get(pk=id)
        hostel.city = request.POST.get('city', hostel.city)
        hostel.address = request.POST.get('address', hostel.address)
        hostel.tax = Tax.objects.get(pk=int(request.POST.get('tax_id', hostel.tax.id)))
        hostel.save()
        return redirect(request.POST.get('back', reverse('hostels:manage_hostels')))

    def delete(self, request, id):
        Hostel.objects.get(pk=id).delete()
        return HttpResponse(status=200)


class ManageBedsView(AdminView):

    def get(self, request):
        beds = Bed.objects.all()
        if 'hostel_id' in request.GET:
            beds = filter(
                (lambda bed: bed.hostel.id == int(request.GET['hostel_id'])),
                beds
            )
        return render(
            request,
            'hostels/manage_beds.html',
            {
                'beds': beds,
                'options': {
                    'tax': [(tax.id, tax.name) for tax in Tax.objects.all()],
                    'gender': Bed.Gender,
                },
            }
        )

    def post(self, request):
        Bed(
            hostel=Hostel.objects.get(pk=int(request.POST['hostel_id'])),
            tax=Tax.objects.get(pk=int(request.POST['tax_id'])),
            actual_order=None,
            gender=int(request.POST['gender'])
        ).save()
        return redirect(request.get_full_path())


class ManageEditBedView(AdminView):

    def post(self, request, id):
        bed = Bed.objects.get(pk=id)
        bed.hostel = Hostel.objects.get(pk=int(request.POST.get('hostel_id', bed.hostel.id)))
        bed.tax = Tax.objects.get(pk=int(request.POST.get('tax_id', bed.tax.id)))
        #bed.actual_order
        bed.gender = int(request.POST.get('gender', bed.gender))
        bed.save()
        return redirect(request.POST.get('back', reverse('hostels:manage_beds')))

    def delete(self, request, id):
        Bed.objects.get(pk=id).delete()
        return HttpResponse(status=200)


class ManageOperatorsView(AdminView):

    def get(self, request):
        operators = Operator.objects.all()
        if 'hostel_id' in request.GET:
            hostel_id = int(request.GET['hostel_id'])
            operators = filter(
                (lambda op: hostel_id in [hostel.id for hostel in op.hostels.all()]),
                operators
            )
        return render(
            request,
            'hostels/manage_operators.html',
            {
                'operators': operators,
                'options': {
                    'hostels': [(hostel, str(hostel)) for hostel in Hostel.objects.all()]
                },
            }
        )

    def post(self, request):
        user = User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password']
        )
        operator = Operator(
            user=user,
            full_name=request.POST['full_name'],
            identification=request.POST['identification'],
            phone_number=request.POST['phone_number'],
            is_admin=bool(int(request.POST.get('is_admin', 0))),
        )
        operator.save()

        for hostel_id in request.POST.getlist('hostels'):
            hostel = Hostel.objects.get(pk=hostel_id)
            operator.hostels.add(hostel)
        operator.save()

        return redirect(request.get_full_path())


class ManageEditOperatorView(AdminView):

    def post(self, request, id):
        operator = Operator.objects.get(pk=id)

        operator.user.username = request.POST.get('username', operator.user.username)
        if 'password' in request.POST:
            operator.user.set_password(request.POST['password'])
            operator.user.save()

        operator.full_name = request.POST.get('full_name', operator.full_name)
        operator.identification = request.POST.get('identification', operator.identification)
        operator.phone_number = request.POST.get('phone_number', operator.phone_number)
        operator.is_admin = bool(int(request.POST.get('is_admin', operator.is_admin)))

        if 'hostels' in request.POST:
            hostels = []
            for hostel_id in request.POST.getlist('hostels'):
                hostel = Hostel.objects.get(pk=int(hostel_id))
                hostels.append(hostel)
            operator.hostels = hostels
            operator.save()

        operator.save()
        return redirect(request.POST.get('back', reverse('hostels:manage_operators')))

    def delete(self, request, id):
        operator = Operator.objects.get(pk=id)
        user.delete()
        operator.delete()
        return HttpResponse(status=200)


class ManageOrdersView(AdminView):

    def get(self, request):
        orders = Order.objects.all()
        if 'hostel_id' in request.GET:
            hostel_id = int(request.GET['hostel_id'])
            orders = filter(
                (lambda order: order.bed.hostel.id == hostel_id),
                orders
            )
        return render(
            request,
            'hostels/manage_orders.html',
            {
                'orders': orders,
                'options': {
                    'beds': [(bed, str(bed)) for bed in Bed.objects.all()],
                    'statuses': Order.Status,
                },
            }
        )

    def post(self, request):
        pass


class ManageEditOrderView(AdminView):

    model = Order
    redirect_url = 'hostels:manage_orders'


class ManageChargesView(AdminView):

    def get(self, request):
        charges = Charge.objects.all()
        if 'hostel_id' in request.GET:
            hostel_id = int(request.GET['hostel_id'])
            charges = filter(
                (lambda charge: charge.order.bed.hostel.id == hostel_id),
                charges
            )
        if 'order_id' in request.GET:
            order_id = int(request.GET['order_id'])
            charges = filter(
                (lambda charge: charge.order.id == order_id),
                charges
            )
        return render(
            request,
            'hostels/manage_charges.html',
            {
                'charges': charges,
                'options': {
                    'reasons': Charge.Reason,
                    'oders': [(order.id, order) for order in Order.objects.all()],
                },
            }
        )

    def post(self, request):
        pass


class ManageEditChargeView(AdminView):

    model = Charge
    redirect_url = 'hostels:manage_charges'


class ManageTaxesView(AdminView):

    def get(self, request):
        taxes = Tax.objects.all()
        return render(
            request,
            'hostels/manage_taxes.html',
            {
                'taxes': taxes,
            }
        )

    def post(self, request):
        pass


class ManageEditTaxView(AdminView):

    model = Tax
    redirect_url = 'hostels:manage_taxes'

class ManageEditTaxGradeView(AdminView):

    model = Tax
    redirect_url = 'hostels:manage_taxes'


class ManageHostelsReportView(AdminView):

    def get(self, request):
        today = datetime.now().date()
        start_date = datetime.strptime(request.GET.get(
            'start_date',
            datetime.strftime(today, '%Y-%m-%d')
        ), '%Y-%m-%d').date()
        end_date = datetime.strptime(request.GET.get(
            'end_date',
            datetime.strftime(today, '%Y-%m-%d')
        ), '%Y-%m-%d').date()

        hostels = Hostel.objects.all()
        for hostel in hostels:
            hostel.report_value_income = hostel.period_value_income(
                start_date=start_date,
                end_date=end_date
            )
            hostel.report_value_outgo = hostel.period_value_outgo(
                start_date=start_date,
                end_date=end_date
            )
            hostel.report_settlements = hostel.period_settlements(
                start_date=start_date,
                end_date=end_date
            )
            hostel.report_departures = hostel.period_departures(
                start_date=start_date,
                end_date=end_date
            )

        return render(
            request,
            'hostels/manage_hostels_report.html',
            {
                'hostels': hostels,
                'start_date': start_date,
                'end_date': end_date,
            }
        )


class ManageChargesHistoryView(AdminView):

    def get(self, request):
        today = datetime.now().date()
        start_date = datetime.strptime(request.GET.get(
            'start_date',
            datetime.strftime(today, '%Y-%m-%d')
        ), '%Y-%m-%d').date()
        end_date = datetime.strptime(request.GET.get(
            'end_date',
            datetime.strftime(today, '%Y-%m-%d')
        ), '%Y-%m-%d').date()

        charges = Charge.objects.filter(
            date__gt=start_date,
            date__lt=end_date
        ).order_by('date')

        return render(
            request,
            'hostels/manage_charges_history.html',
            {
                'charges': charges,
                'start_date': start_date,
                'end_date': end_date,
            }
        )


class ManageOrdersHistoryView(AdminView):

    def get(self, request):
        today = datetime.now().date()
        start_date = datetime.strptime(request.GET.get(
            'start_date',
            datetime.strftime(today, '%Y-%m-%d')
        ), '%Y-%m-%d').date()
        end_date = datetime.strptime(request.GET.get(
            'end_date',
            datetime.strftime(today, '%Y-%m-%d')
        ), '%Y-%m-%d').date()
        return render(
            request,
            'hostels/manage_orders_history.html',
            {
                'orders': [
                    x for x in OrderHistory.objects.all()
                        if start_date <= x.history_start.date() <= end_date
                ],
                'start_date': start_date,
                'end_date': end_date,
            }
        )


class ManageTaxesHistoryView(AdminView):

    def get(self, request):
        today = datetime.now().date()
        start_date = datetime.strptime(request.GET.get(
            'start_date',
            datetime.strftime(today, '%Y-%m-%d')
        ), '%Y-%m-%d').date()
        end_date = datetime.strptime(request.GET.get(
            'end_date',
            datetime.strftime(today, '%Y-%m-%d')
        ), '%Y-%m-%d').date()
        return render(
            request,
            'hostels/manage_taxes_history.html',
            {
                'taxes': [
                    x for x in TaxHistory.objects.all()
                        if start_date <= x.history_start.date() <= end_date
                ],
                'start_date': start_date,
                'end_date': end_date,
            }
        )


#########################
###                   ### 
###   Utility views   ###
###                   ###
#########################


class UtilCleanupOldDataView(View):

    def get(self, request):
        utils.cleanup_old_data()
        return HttpResponse(status=200)


class UtilRefreshAllBedsView(View):

    def get(self, request):
        utils.refresh_all_beds()
        return HttpResponse(status=200)

