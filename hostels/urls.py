# -*- conding: utf-8 -*-
from django.conf.urls import url

from . import views


app_name = 'hostels'
urlpatterns = [

    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^logout/$', views.Logout.as_view(), name='logout'),


    ###   Operator URLs   ###

    url(r'^beds/$', views.BedListView.as_view(), name='bed_list'),
    url(r'^bed/(?P<bed_id>\d+)/create_order$', views.CreateActualOrderView.as_view(), name='create_actual_order'),
    url(r'^bed/(?P<bed_id>\d+)/tax_value$', views.BedTaxValueView.as_view(), name='bed_tax_value'),
    url(r'^bed/(?P<bed_id>\d+)/change_end_date$', views.ChangeOrderEndDateView.as_view(), name='change_order_end_date'),
    url(r'^bed/(?P<bed_id>\d+)/reservation$', views.CreateReservationView.as_view(), name='create_reservation'),
    url(r'^bed/(?P<bed_id>\d+)/confirm_completion$', views.ConfirmCompletionView.as_view(), name='confirm_completion'),
    url(r'^bed/(?P<bed_id>\d+)/activate_reservation$', views.ActivateReservationView.as_view(), name='activate_reservation'),
    url(r'^bed/(?P<bed_id>\d+)/cancel_reservation$', views.CancelReservationView.as_view(), name='cancel_reservation'),

    url(r'^reservation_calendar$', views.ReservationCalendarView.as_view(), name='reservation_calendar'),
    url(r'^taxes$', views.TaxesView.as_view(), name='tax_list'),
    url(r'^orders$', views.OrderListView.as_view(), name='order_list'),
    url(r'^hostels$', views.HostelListView.as_view(), name='hostel_list'),

    url(r'^order/(?P<order_id>\d+)/remove_reservation$', views.RemoveReservationView.as_view(), name='remove_reservation'),
    url(r'^order/(?P<order_id>\d+)/change_dates$', views.ChangeReservationDatesView.as_view(), name='change_reservation_dates'),


    ###   Manager URLs   ###

    url(r'^manage/$', views.ManageIndexView.as_view(), name='manage_index'),
    url(r'^manage/hostels/$', views.ManageHostelsView.as_view(), name='manage_hostels'),
    url(r'^manage/hostels/report', views.ManageHostelsReportView.as_view(), name='manage_hostels_report'),
    url(r'^manage/beds/$', views.ManageBedsView.as_view(), name='manage_beds'),
    url(r'^manage/operators/$', views.ManageOperatorsView.as_view(), name='manage_operators'),
    url(r'^manage/orders/$', views.ManageOrdersView.as_view(), name='manage_orders'),
    url(r'^manage/orders/history$', views.ManageOrdersHistoryView.as_view(), name='manage_orders_history'),
    url(r'^manage/charges/$', views.ManageChargesView.as_view(), name='manage_charges'),
    url(r'^manage/charges/history$', views.ManageChargesHistoryView.as_view(), name='manage_charges_history'),
    url(r'^manage/taxes/$', views.ManageTaxesView.as_view(), name='manage_taxes'),
    url(r'^manage/taxes/history$', views.ManageTaxesHistoryView.as_view(), name='manage_taxes_history'),

    url(r'^manage/hostel/(?P<id>\d+)$', views.ManageEditHostelView.as_view(), name='manage_edit_hostel'),
    url(r'^manage/bed/(?P<id>\d+)$', views.ManageEditBedView.as_view(), name='manage_edit_bed'),
    url(r'^manage/operator/(?P<id>\d+)$', views.ManageEditOperatorView.as_view(), name='manage_edit_operator'),
    url(r'^manage/order/(?P<id>\d+)$', views.ManageEditOrderView.as_view(), name='manage_edit_order'),
    url(r'^manage/charge/(?P<id>\d+)$', views.ManageEditChargeView.as_view(), name='manage_edit_charge'),
    url(r'^manage/tax/(?P<id>\d+)$', views.ManageEditTaxView.as_view(), name='manage_edit_taxes'),
    url(r'^manage/taxgrade/(?P<id>\d+)$', views.ManageEditTaxGradeView.as_view(), name='manage_edit_tax_grades'),




    ###   Utility URLs   ###

    url(r'^util/cleanup_old_data$', views.UtilCleanupOldDataView.as_view(), name='util_cleanup_old_data'),
    url(r'^util/refresh_all_beds$', views.UtilRefreshAllBedsView.as_view(), name='util_update_all_beds'),

]