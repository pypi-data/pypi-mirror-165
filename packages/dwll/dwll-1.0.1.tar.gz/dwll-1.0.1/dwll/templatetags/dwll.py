# -*- coding: utf-8 -*-
"""
.. module:: dbu-maintags
   :platform: Unix, Windows
   :synopsis: Tags del modulo DBU

.. moduleauthor:: Diego Gonzalez <dgonzalez.jim@gmail.com>

"""
from django import template
from django.utils.safestring import mark_safe

from dwll import messages
from dwll import configuration
from dwll.languages import languages

register = template.Library()

@register.simple_tag(takes_context=True)
def display_message(context, name, default=None):
    """
    Tag para mostrar un mensaje previamente almacenado en BDD
    y memoria, en pantalla formateado en HTML

    :param request: Request Actual
    :param name: Nombre del Mensaje
    :return: String -- Mensaje HTML

    """
    request = context['request']
    language = languages.get_language(request)
    return mark_safe( messages.get_message(name, language, default=default) )

@register.simple_tag(takes_context=True)
def get_configuration(context, name, default=None):
    """
    Tag para obtener una configuracion previamente almacenada en BDD
    y memoria

    :param name: Nombre de la configuracion
    :param default: Valor por defecto
    :return: String -- Valor de Configuracion

    """
    return configuration.get_value(name, default=default)

@register.simple_tag(takes_context=True)
def get_configuration_as_bool(context, name, true_value, default=None):
    """
    Tag para obtener una configuracion en formato booleano basado en el valor verdadero
    pasado en este template

    :param name: Nombre de la configuracion
    :param true_value: Valor verdadero
    :param default: Valor por defecto
    :return: String -- Mensaje HTML

    """
    return configuration.get_value(name, default=default) == true_value


@register.simple_tag(takes_context=True)
def get_languages(context):
    """
    Return the languages list
    """
    request = context['request']
    return languages.get_languages_list(request)