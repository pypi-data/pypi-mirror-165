# -*- coding: utf-8 -*-
"""
.. module:: dbu-impexp
   :platform: Unix, Windows
   :synopsis: Import Export resources for dbu module

.. moduleauthor:: Diego Gonzalez <dgonzalez.jim@gmail.com>

"""
from import_export import resources

from . import models

class ConfigurationResource(resources.ModelResource):
    """

    Configuration Resource
    ===================

    Description
        Recurso para exportar o importar datos del modelo
        Configuration.

    """

    class Meta:
        model = models.Configuration

class MessageResource(resources.ModelResource):
    """

    Message Resource
    ===================

    Description
        Recurso para exportar o importar datos del modelo
        Message.

    """

    class Meta:
        model = models.Message

class MessageTraductionResource(resources.ModelResource):
    """

    Message Resource
    ===================

    Description
        Recurso para exportar o importar datos del modelo
        MessageTraduction.

    """

    class Meta:
        model = models.MessageTraduction