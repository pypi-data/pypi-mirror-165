# -*- coding: utf-8 -*-
"""
.. module:: dbu - context
   :platform: Unix, Windows
   :synopsis: Contexto Principal por defecto

.. moduleauthor:: Diego Gonzalez <dgonzalez.jim@gmail.com>

"""
from . import configuration
from . import models


def load_context(request):
    """

    Load Context

    Description
        Carga las variables de contexto principales

    :param request:
    :return:
    """

    IS_TEST_MODE = configuration.isTESTMode()

    IS_MAINTENANCE = configuration.isMaintenanceMode()

    try:
        LANGUAGES = models.Language.objects.get_active()
    except:
        LANGUAGES = []

    return {
        'IS_TEST_MODE' : IS_TEST_MODE,
        'IS_MAINTENANCE' : IS_MAINTENANCE,
        'LANGUAGES' : LANGUAGES
    }