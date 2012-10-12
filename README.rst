=====================
django_localflavor_pe
=====================

Country-specific Django helpers for Peru.

What's in the Peru localflavor?
===============================

* forms.PEDNIField: A form field that validates input as a DNI (Peruvian
  national identity) number.

* forms.PERUCField: A form field that validates input as an RUC (Registro
  Unico de Contribuyentes) number. Valid RUC numbers have 11 digits.

* forms.PEDepartmentSelect: A ``Select`` widget that uses a list of Peruvian
  Departments as its choices.

See the source code for full details.

About localflavors
==================

Django's "localflavor" packages offer additional functionality for particular
countries or cultures.

For example, these might include form fields for your country's postal codes,
phone number formats or government ID numbers.

This code used to live in Django proper -- in django.contrib.localflavor -- but
was separated into standalone packages in Django 1.5 to keep the framework's
core clean.

For a full list of available localflavors, see https://github.com/django/
