# -*- coding: utf-8 -*-
"""
PE-specific Form helpers.
"""

from __future__ import absolute_import, unicode_literals

from django.contrib.localflavor.pe.pe_region import REGION_CHOICES
from django.core.validators import EMPTY_VALUES
from django.forms import ValidationError
from django.forms.fields import RegexField, CharField, Select
from django.utils.translation import ugettext_lazy as _


class PERegionSelect(Select):
    """
    A Select widget that uses a list of Peruvian Regions as its choices.
    """
    def __init__(self, attrs=None):
        super(PERegionSelect, self).__init__(attrs, choices=REGION_CHOICES)


class PEDNIField(CharField):
    """
    A field that validates Documento Nacional de Identidad (DNI | National
    Identity Document) numbers.
    """
    default_error_messages = {
        'invalid': _('This field requires only numbers.'),
        'max_digits': _('This field requires 8 digits.'),
    }

    def __init__(self, max_length=8, min_length=8, *args, **kwargs):
        super(PEDNIField, self).__init__(max_length, min_length, *args,
                                         **kwargs)

    def clean(self, value):
        """
        Value must be a string in the XXXXXXXX format.
        """
        value = super(PEDNIField, self).clean(value)
        if value in EMPTY_VALUES:
            return ''
        if not value.isdigit():
            raise ValidationError(self.error_messages['invalid'])
        if len(value) != 8:
            raise ValidationError(self.error_messages['max_digits'])

        return value


class PERUCField(RegexField):
    """
    This field validates a RUC (Registro Unico de Contribuyentes | Unique
    Contributor Registry).

    Based in the actual RUC Validation Procedure used by SUNAT's
    (SUperintendencia Nacional de Administración Tributaria | National
    Tributary Administration Superintendence) portal; Specifically in their JS
    validation script located at http://www.sunat.gob.pe/a/js/js.js tells that
    there can be two kinds of RUC: One of 8 digits and another with 11.

    Validation algorithms for both are implemented here.
    """
    default_error_messages = {
        'invalid_input': _('This field requires only numbers.'),
        'wrong_number_of_digits': _('This field requires 8 or 11 '
                                    'digit numbers.'),
        'invalid_number': _('RUC number invalid.')
    }

    def __init__(self, max_length=11, min_length=8, *args, **kwargs):
        super(PERUCField, self).__init__(max_length, min_length, *args,
                                         **kwargs)

    def clean(self, value):
        """
        Value must be an 11 or 8 digit number and must be validated against a
        couple of algorithms.
        """
        value = super(PERUCField, self).clean(value)
        if value in EMPTY_VALUES:
            return ''
        if not value.isdigit():
            raise ValidationError(self.error_messages['invalid_input'])
        if len(value) not in (8, 11,):
            raise ValidationError(self.error_messages['wrong_number_of_digits'])
        if not self.ruc_is_valid(value):
            raise ValidationError(self.error_messages['invalid_number'])
        return value

    def ruc_is_valid(self, value):
        """
        Ripped and pythonized directly from http://www.sunat.gob.pe/a/js/js.js
        """

        length = len(value)
        if length == 8:
            digit_sum = 0
            for pos in range(length - 1):
                if pos == 0:
                    digit_sum = int(value[0]) * 2
                else:
                    digit_sum += int(value[pos]) * (length - pos)

            modulo = digit_sum % 11
            if modulo == 1:
                modulo = 11
            if modulo + int(value[-1]) == 11:
                return True

        elif length == 11:
            digit_sum = 0
            x = 6
            for pos in range(length - 1):
                if pos == 4:
                    x = 8
                x -= 1
                # The original JS is kinda strange in this part.
                digit_sum += int(value[pos]) * x

            modulo = 11 - (digit_sum % 11)

            if modulo >= 10:
                modulo -= 10
            if modulo == int(value[-1]):
                return True

        return False
