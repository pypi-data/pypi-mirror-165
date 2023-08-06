# -*- coding: utf-8 -*-
"""
.. module:: dbu-configuration
   :platform: Unix, Windows
   :synopsis: Manager para variables de configuracion

.. moduleauthor:: Diego Gonzalez <dgonzalez.jim@gmail.com>

"""
from . import models

class ConfigurationManager:
    """

    Configuration Manager
    ===================

    Description
        Manejador de variables de configuracion, esta clase permite
        acceder a dichas variables y mantenerlas en cache.

        Solo se puede reflejar el cambio del valor de la configuracion
        desde el administrador luego de reiniciar el servidor de aplicaciones.

    """

    # Valor por defecto al crear una variable de configuracion
    DEFAULT_VALUE = '0'

    # Longitud minima de los nombres
    MAX_NAME_SIZE = 50

    # Longitud maxima de los nombres
    MAX_DESC_SIZE = 150

    # Valor por defecto usado en la configuracion del MODO
    MAIN_CONFIG_WORMODE_DEFAULT = 'TEST'

    # El sistema se encuentra en modo mantenimiento
    MAIN_CONFIG_WORMODE_MAINTENANCE = 'MANT'

    # Diccionario de Configuraciones principales de Multipasajes
    # Siempre el primero de los valores es el valor por defecto
    MAIN_CONFIGURATION = [
        {
            'name': 'common.workmode',
            'desc': 'Multipasajes Execution Mode',
            'values': [MAIN_CONFIG_WORMODE_DEFAULT, 'PROD']
        }
    ]

    def get_value(self, name, description='N/A', default=None):
        """

        Get Value

        Description
            Dado el nombre, devuelve el valor de un registro de
            configuracion, mantiene en memoria los valores.

        :return
            String -- El texto del mensaje

        """
        try:
            value = self.DEFAULT_VALUE

            if hasattr(get_value, 'values'):
                value_dict = get_value.values
            else:
                value_dict = {}

            if name in value_dict:
                value = value_dict[name]
            else:
                values = models.Configuration.objects.get_active(name=name)
                if values.count() > 0:
                    value = values.first().value
                    value_dict[name] = value
                    get_value.values = value_dict
                else:
                    self.create_default(name, description, default)
                    value = default

            return value
        except Exception as e:
            return ''

    def create_default(self, name, description, default):
        """

        Create Default

        Description
            Permite crear un parametro de configuracion por defecto en caso
            de que no exista, asi estara disponible para que el administrador
            ingrese el valor correcto

        @param name:
        @param description:
        @param default: Este es el valor por defecto para la creacion de una variable

        """
        try:
            if len(name) <= self.MAX_NAME_SIZE:
                is_config, main_config = self.is_main_config(name)
                if is_config:
                    models.Configuration.objects.create(name=name, value=main_config['values'][0],
                                                        description=self.get_main_config_description(main_config))
                else:
                    value = default if default else ''
                    models.Configuration.objects.create(name=name, value=value,
                                                        description=description[:self.MAX_DESC_SIZE]
                                                        if description else 'N/A')

        except Exception as e:
            print('<-- Error al crear la configuracion por defecto: %s' % str(e))

    def is_main_config(self, name):
        """

        Is Main Config

        Description
            Verifica si la configuracion es principal

        @param name:
        @return True si es principal
        """
        for mc in self.MAIN_CONFIGURATION:
            if mc['name'] == name:
                return True, mc
        return False, None

    def get_main_config_description(self, main_config):
        """

        Get Main Config Description

        Description
            Arma una descripcion con los posibles valores de la configuracion

        @param main_config:
        @return String -- Formato de descripcion estandar
        """
        return '%s [%s]' % (main_config['desc'], ','.join([v for v in main_config['values']]))

cmanager = ConfigurationManager()

def get_value(name, default=None, description=None):
    """

    Get Value

    Description
        Acceso rapido a las configuraciones

    :param name: El nombre unico del parametro
    :return: String -- El valor
    """
    return ConfigurationManager().get_value(name, description=description, default=default)

def get_float(name, default=None, description=None):
    """

    Get Float

    Description
        Acceso rapido a una configuracion como numero flotante

    :param name: El nombre unico del parametro
    :return: Float -- El valor
    """
    try:
        return float(ConfigurationManager().get_value(name, description=description, default=default))
    except:
        return 0

def get_integer(name, default=None, description=None):
    """

    Get Float

    Description
        Acceso rapido a una configuracion como numero entero

    :param name: El nombre unico del parametro
    :return: Integer -- El valor
    """
    try:
        return int(ConfigurationManager().get_value(name, description=description, default=default))
    except:
        return 0

def isTESTMode():
    """

    Is Test Mode

    Description
        Valida si la configuracion del sistema se encuentra en modo TEST

    :return: True si estamos en modo TEST
    """
    return str(ConfigurationManager().get_value('common.workmode', 
            default=ConfigurationManager.MAIN_CONFIG_WORMODE_DEFAULT)) == \
           str(ConfigurationManager.MAIN_CONFIG_WORMODE_DEFAULT)

def isMaintenanceMode():
    """

    Is Maintenance Mode

    Description
        Valida si la configuracion del sistema se encuentra en modo MANTENIMIENTO

    :return: True si estamos en modo MANTENIMIENTO
    """
    return str(ConfigurationManager().get_value('common.workmode')) == \
           str(ConfigurationManager.MAIN_CONFIG_WORMODE_MAINTENANCE)
