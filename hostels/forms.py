# -*- conding: utf-8 -*-
from django import forms


COMMON_ERROR_MESSAGES = {
    'required': 'Обязательное поле',
    'invalid': 'Некорректное значение',
}


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Логин:',
        error_messages=COMMON_ERROR_MESSAGES
    )
    password = forms.CharField(
        label='Пароль:',
        widget=forms.PasswordInput,
        error_messages=COMMON_ERROR_MESSAGES
    )


##########################
###                    ###
###   Operator forms   ###
###                    ###
##########################


class ActualOrderForm(forms.Form):
    start_date = forms.DateField(
        label='Дата въезда:',
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
        error_messages=COMMON_ERROR_MESSAGES
    )
    end_date = forms.DateField(
        label='Дата отъезда:',
        error_messages=COMMON_ERROR_MESSAGES
    )
    guest_full_name = forms.CharField(
        label='ФИО гостя:',
        error_messages=COMMON_ERROR_MESSAGES
    )
    guest_identification = forms.CharField(
        label='Паспортные данные гостя:',
        error_messages=COMMON_ERROR_MESSAGES
    )
    guest_phone_number = forms.CharField(
        label='Номер телефона гостя:',
        error_messages=COMMON_ERROR_MESSAGES
    )
    value = forms.FloatField(
        label='Сумма:',
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
        required=False,
        error_messages=COMMON_ERROR_MESSAGES
    )


class ChangeOrderEndDateForm(forms.Form):
    start_date = forms.DateField(
        label='Дата въезда:',
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
        required=False,
        error_messages=COMMON_ERROR_MESSAGES
    )
    end_date = forms.DateField(
        label='Дата отъезда:',
        error_messages=COMMON_ERROR_MESSAGES
    )
    old_value = forms.FloatField(widget=forms.HiddenInput())
    value = forms.FloatField(
        label='Доплата:',
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
        required=False,
        error_messages=COMMON_ERROR_MESSAGES
    )


class ReservationForm(forms.Form):
    start_date = forms.DateField(
        label='Дата въезда:',
        error_messages=COMMON_ERROR_MESSAGES
    )
    end_date = forms.DateField(
        label='Дата отъезда:',
        error_messages=COMMON_ERROR_MESSAGES
    )
    guest_full_name = forms.CharField(
        label='ФИО гостя:',
        error_messages=COMMON_ERROR_MESSAGES
    )
    guest_identification = forms.CharField(
        label='Паспортные данные гостя:',
        error_messages=COMMON_ERROR_MESSAGES
    )
    guest_phone_number = forms.CharField(
        label='Номер телефона гостя:',
        error_messages=COMMON_ERROR_MESSAGES
    )
    value = forms.FloatField(
        label='Сумма:',
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
        required=False,
        error_messages=COMMON_ERROR_MESSAGES
    )


class ConfirmCompletionForm(forms.Form):
    start_date = forms.DateField(
        label='Дата въезда:',
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
        error_messages=COMMON_ERROR_MESSAGES
    )
    end_date = forms.DateField(
        label='Дата отъезда:',
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
        error_messages=COMMON_ERROR_MESSAGES
    )
    guest_full_name = forms.CharField(
        label='ФИО гостя:',
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
        error_messages=COMMON_ERROR_MESSAGES
    )
    guest_identification = forms.CharField(
        label='Паспортные данные гостя:',
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
        error_messages=COMMON_ERROR_MESSAGES
    )
    guest_phone_number = forms.CharField(
        label='Номер телефона гостя:',
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
        error_messages=COMMON_ERROR_MESSAGES
    )
    value = forms.FloatField(
        label='Сумма:',
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
        error_messages=COMMON_ERROR_MESSAGES
    )


class ActivateReservationForm(forms.Form):
    start_date = forms.DateField(
        label='Дата въезда:',
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
        error_messages=COMMON_ERROR_MESSAGES
    )
    end_date = forms.DateField(
        label='Дата отъезда:',
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
        error_messages=COMMON_ERROR_MESSAGES
    )
    guest_full_name = forms.CharField(
        label='ФИО гостя:',
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
        error_messages=COMMON_ERROR_MESSAGES
    )
    guest_identification = forms.CharField(
        label='Паспортные данные гостя:',
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
        error_messages=COMMON_ERROR_MESSAGES
    )
    guest_phone_number = forms.CharField(
        label='Номер телефона гостя:',
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
        error_messages=COMMON_ERROR_MESSAGES
    )
    value = forms.FloatField(
        label='Сумма:',
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
        error_messages=COMMON_ERROR_MESSAGES
    )


class CancelReservationForm(forms.Form):
    start_date = forms.DateField(
        label='Дата въезда:',
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
        error_messages=COMMON_ERROR_MESSAGES
    )
    end_date = forms.DateField(
        label='Дата отъезда:',
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
        error_messages=COMMON_ERROR_MESSAGES
    )
    guest_full_name = forms.CharField(
        label='ФИО гостя:',
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
        error_messages=COMMON_ERROR_MESSAGES
    )
    guest_identification = forms.CharField(
        label='Паспортные данные гостя:',
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
        error_messages=COMMON_ERROR_MESSAGES
    )
    guest_phone_number = forms.CharField(
        label='Номер телефона гостя:',
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
        error_messages=COMMON_ERROR_MESSAGES
    )
    value = forms.FloatField(
        label='Сумма:',
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
        error_messages=COMMON_ERROR_MESSAGES
    )


class RemoveReservationForm(forms.Form):
    status = forms.CharField(
        label='Статус:',
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
    )
    start_date = forms.DateField(
        label='Дата въезда:',
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
    )
    end_date = forms.DateField(
        label='Дата отъезда:',
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
    )
    guest_full_name = forms.CharField(
        label='ФИО гостя:',
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
    )
    guest_identification = forms.CharField(
        label='Паспортные данные гостя:',
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
    )
    guest_phone_number = forms.CharField(
        label='Номер телефона гостя:',
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
    )
    value = forms.FloatField(
        label='Сумма:',
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
    )


class EditReservationDatesForm(forms.Form):
    status = forms.CharField(
        label='Статус:',
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
    )
    start_date = forms.DateField(
        label='Дата въезда:',
    )
    end_date = forms.DateField(
        label='Дата отъезда:',
    )
    guest_full_name = forms.CharField(
        label='ФИО гостя:',
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
    )
    guest_identification = forms.CharField(
        label='Паспортные данные гостя:',
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
    )
    guest_phone_number = forms.CharField(
        label='Номер телефона гостя:',
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
    )
    value = forms.FloatField(
        label='Сумма:',
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
    )


#########################
###                   ###
###   Manager forms   ###
###                   ###
#########################


