from django import forms

from . import messages, properties as P

import re

class CommonForm:

    """

    Utilitarios para formularios estandares bootstrap

    """

    def __init__(self):
        """

        Construye estimando que request puede ser nulo

        """
        self.request = None

    def get_module(self):
        """

        Metodo a sobrecargar

        :return:
        """
        return 'common'

    def attrs_apply(self, name, onchange, rule, msg):
        """

        Aplica otros atributos

        :param name:
        :param onchange:
        :param rule:
        :param msg:
        :return:
        """
        if onchange:
            self.fields[name].widget.attrs[onchange] = onchange

        if rule:
            self.fields[name].widget.attrs['data-rule'] = rule

        if msg:
            self.fields[name].widget.attrs['data-msg'] = msg
        else:
            self.fields[name].widget.attrs['data-msg'] = messages.get_full_message(self.request,
                                                                                   'forms.field.error.%s' % name)

    def text_config(self, name, rule=None, msg=None, onchange=None):
        """

        Text Config

        Description
            Configuracion de texto

        :param name:
        :return:
        """
        self.fields[name].widget.attrs = {
            'class':'form-control',
            'data-placement':'left',
            'placeholder': messages.get_full_message(self.request, 'forms.field.placeholder.%s' % name),
        }

        self.attrs_apply(name, onchange, rule, msg)

    def choices_config(self, name, choices, required=False, rule=None, msg=None, onchange=None):
        """

        Choices Field Config

        Description
            Configuracion de listado

        :param name:
        :return:
        """
        self.fields[name] = forms.ChoiceField(choices=choices, required=required, widget=forms.Select(attrs={
            'class': 'form-control',
            'data-placement': 'left',
            'placeholder': messages.get_full_message(self.request, 'forms.field.placeholder.%s' % name)
        }))

        self.attrs_apply(name, onchange, rule, msg)

    def datetime_config(self, name, input_formats=P.DATETIME_INPUT_FORMATS, rule=None, msg=None, required=True, onchange=None):
        """

        Date Config

        Description
            Configuracion de fechas

        :param name:
        :return:
        """
        self.fields[name] = forms.DateField(input_formats=input_formats, widget=forms.DateInput(
            attrs={
                'class': 'date form-control datepicker',
                'data-placement': 'left',
                'type':'datetime-local'
            }
        ), required=required)

        self.attrs_apply(name, onchange, rule, msg)

    def date_config(self, name, input_formats=P.DATE_INPUT_FORMATS, rule=None, msg=None, required=True, onchange=None):
        """

        Date Config

        Description
            Configuracion de fechas

        :param name:
        :return:
        """
        self.fields[name] = forms.DateField(input_formats=input_formats, widget=forms.DateInput(
            attrs={
                'class': 'date form-control datepicker',
                'data-placement': 'left',
                'type':'date'
            },
            format=('%m-%d-%Y')
        ), required=required)

        self.attrs_apply(name, onchange, rule, msg)

    def boolean_config(self, name, rule=None, msg=None, required=True, onchange=None):
        """

        Boolean Config

        Description
            Configuracion de booleanos

        :param name:
        :return:
        """
        self.fields[name] = forms.BooleanField(required=required)

        self.fields[name].widget.attrs = {
            'class': 'form-control',
            'data-placement': 'left',
            'autocomplete': 'off',
            'placeholder': messages.get_full_message(self.request, 'forms.field.placeholder.%s' % name)
        }

        self.attrs_apply(name, onchange, rule, msg)

    def decimal_config(self, name, rule=None, msg=None, step='0.01', onchange=None):
        """

        Decimal Config

        Description
            Configuracion de texto

        :param name:
        :return:
        """
        self.fields[name].widget.attrs = {
            'step':step,
            'class':'money-input form-control',
            'data-placement':'left',
            'placeholder': messages.get_full_message(self.request, 'forms.field.placeholder.%s' % name)
        }

        self.attrs_apply(name, onchange, rule, msg)

    def integer_config(self, name, rule=None, msg=None, onchange=None):
        """

        Integer Config

        Description
            Configuracion de numero entero

        :param name:
        :return:
        """
        self.fields[name].widget.attrs = {
            'step':'1',
            'class':'money-input form-control',
            'data-placement':'left',
            'placeholder': messages.get_full_message(self.request, 'forms.field.placeholder.%s' % name)
        }

        self.attrs_apply(name, onchange, rule, msg)

    def is_alphanumeric(self, text):
        """

        Valida si es solo texto y numeros sin caracteres especiales

        :param text:
        :return:
        """
        return re.match("^[a-zA-Z0-9_]*$", text) and ' ' not in text
