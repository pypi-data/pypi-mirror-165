# -*- coding: utf-8 -*-
"""
.. module:: commons
   :platform: Unix, Windows
   :synopsis: Ajax base class

.. moduleauthor:: Diego Gonzalez <dgonzalez.jim@gmail.com>

"""

import uuid

class AjaxBase:

    params = {}
    exist_all = True

    DEBUG = False

    def ID(self):
        """

        Description
            Devuelve un ID Unico a ser usado por el resto de metodos
            para evitar obtener parametros con valores cambiados

        :return:
        """
        id = uuid.uuid4().int & (1<<32)-1
        id = str(id)[:8]
        if self.DEBUG:print('==> {AJAX REQUEST #', id,'}')
        return id

    def GET(self, id, request, attributes):
        """

        GET Params

        Description
            Dada una lista de atributos, construye un diccionario
            de los parametros pasados por GET

        @param attributes List - String
        """
        for p in attributes:
            if p in request.GET:
                self.params['%s-%s' % (p, id)] = request.GET.get(p)
            else:
                if self.DEBUG:print('<== [AjaxBase.GET] No fue dado', p)
                self.exist_all = False

    def E(self, id, names=None):
        """

        Exist

        Description
            Existe una lista de parametros en params

        :param names:
        :return: True Si existen todos, False si no existe al menos uno
        """
        if names:
            for name in names:
                key = '%s-%s' % (name, id)
                if key not in self.params:
                    return False
            return True
        else:
            return self.exist_all

    def V(self, id, name):
        """

        Value

        Description
            Devuelve el valor de un parametro

        :param name:
        :return:
        """
        key = '%s-%s' % (name, id)
        if key in self.params:
            return self.params[key]
        return None

    def fail(self, error_msg='', method='', info=None):
        """

        Fail

        Description
            Respuesta de error

        :param error_msg:
        :param method:
        :return:
        """
        info = info if info else self.params
        return {
            'success': False,
            'message': error_msg,
            'info':info,
            'method': method,
        }

    def success(self, info=None, method=''):
        """

        Fail

        Description
            Respuesta de error

        :param info: Dictionary
        :param method:
        :return:
        """
        info = info if info else self.params
        return {
            'success': True,
            'message':'OK',
            'info':info,
            'method':method
        }
