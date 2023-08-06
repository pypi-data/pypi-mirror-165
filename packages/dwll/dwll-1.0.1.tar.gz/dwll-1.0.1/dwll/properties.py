# -*- coding: utf-8 -*-
"""
.. module:: dbu-properties
   :platform: Unix, Windows
   :synopsis: Propiedades Generales

.. moduleauthor:: Diego Gonzalez <dgonzalez.jim@gmail.com>

"""

"""

Status

Description
    Estados generales a ser usados por AuditMixin para
    todos los modelos del sistema. Esto sirve para realizar
    eliminacion logica.

"""

ACTIVE = '1'
INACTIVE = '2'

# Formato de Fecha Principal
DATE_INPUT_FORMAT = '%m/%d/%Y'

"""

Date Input Format

Description
    El formato a ser usado por todos los campos de tipo
    fecha en los formularios del sistema.

"""

DATE_INPUT_FORMATS = ['%m/%d/%Y','%m/%d/%y','%Y-%m-%d']
DATETIME_INPUT_FORMATS = ['%m/%d/%Y %H:%M','%m/%d/%y %H:%M','%Y-%m-%d %H:%M']