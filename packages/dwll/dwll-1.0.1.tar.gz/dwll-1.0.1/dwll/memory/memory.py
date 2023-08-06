# -*- coding: utf-8 -*-
"""
.. module:: dbu-memory
   :platform: Unix, Windows
   :synopsis: Helpers Principal de Memoria

.. moduleauthor:: Diego Gonzalez <dgonzalez.jim@gmail.com>

"""
from dwll.memory import constants as C

class Memory:
    """

    Memory
    ===================

    Description
        Helper/Manager para mantener centralizado el registro
        en memoria cache.

    """

    def __init__(self):
        """

        INIT

        :return:
        """
        self.load()
        self.request = None

    def set_request(self, request):
        self.request = request
        return self

    def load(self, step=None):
        """

        Load

        Descriptionself.assertEqual(value, "VALUE1")
            Inicializa el diccionario primario

        :return:
        """
        if not step:
            self.cache_dict = {}
            self.cache_dict[C.MAIN] = {}
        else:
            if not self.cache_dict:
                self.cache_dict = {}
            self.cache_dict[step] = {}

    def store(self, key, value, step=C.MAIN):
        """

        Store

        Description
            Almacena en la clave de un paso del diccionario
            un nuevo valor.

        :param step:
        :param key:
        :param value:
        :param request:
        :return:
        """

        if not self.cache_dict or step not in self.cache_dict:
            self.load(step)

        if self.request:
            sd = self.cache_dict[step]
            sd[key] = value
            self.request.session[C.MASTER_NAME] = self.cache_dict
            self.request.session.modified = True

        self.show()

        return value

    def recover(self, key, sub_key=None, default_value=None, step=C.MAIN):
        """

        Recover

        Description
            Recupera de la clave de un paso del diccionario
            un valor previamente almacenado.

        :param step:
        :param key:
        :param request:
        :return:
        """

        if self.request:
            self.cache_dict = self.request.session[C.MASTER_NAME] if C.MASTER_NAME in self.request.session else None

            if self.cache_dict and step in self.cache_dict and key in self.cache_dict[step]:
                if sub_key:
                    if sub_key in self.cache_dict[step][key]:
                        return self.cache_dict[step][key][sub_key]
                    return None
                else:
                    return self.cache_dict[step][key]
            elif default_value:
                return self.store(key, default_value, step=step)

        return None

    def update(self, key, value, sub_key=None, step=C.MAIN):
        """

        Update

        Description
            Actualiza o agrega un valor en un sub-diccionario almacenado
            en el diccionario principal de la memoria cache.

        :param step:
        :param key:
        :param sub_key:
        :param value:
        :param request:
        :return:
        """
        subd_dict = None

        if self.request:
            if sub_key:
                subd_dict = self.recover(key, step=step)
                subd_dict = subd_dict if subd_dict else {}
                subd_dict[sub_key] = value
            else:
                subd_dict = value

            self.store(key, subd_dict, step=step)

        self.show()

        return subd_dict

    def clean(self, request, key=None, sub_key=None, step=None):
        """

        Clean

        Description
            Limpia de la memoria o del diccionario dependiendo de
            la clave o el paso dados. Si no son dados ninguno de
            ellos se limpia toda la sesion principal.

        :param step:
        :param key:
        :param request:
        :return:
        """

        if request:
            self.cache_dict = request.session[C.MASTER_NAME] if C.MASTER_NAME in request.session else None

            if self.cache_dict:
                if step and key and sub_key:
                    try:
                        del self.cache_dict[step][key][sub_key]
                        request.session[C.MASTER_NAME] = self.cache_dict
                    except:
                        print('[Memory.clean] No se puede limpiar la cache para (', step, key, sub_key, ')')
                elif step and key:
                    try:
                        del self.cache_dict[step][key]
                        request.session[C.MASTER_NAME] = self.cache_dict
                    except:
                        print('[Memory.clean] No se puede limpiar la cache para (', step, key, ')')
                elif step:
                    try:
                        del self.cache_dict[step]
                        request.session[C.MASTER_NAME] = self.cache_dict
                    except:
                        print('[Memory.clean] No se puede limpiar la cache para (', step, ')')
                else:
                    try:
                        del request.session[C.MASTER_NAME]
                    except:
                        print('[Memory.clean] No se puede limpiar la cache total.')
            else:
                print('[Memory.clean] No hay Cache Dict')

        self.show()

    def show(self):
        """

        Show

        Description
            Imprime el diccionario de la memoria

        :return:
        """

        if self.request:
            self.cache_dict = self.request.session[C.MASTER_NAME] if C.MASTER_NAME in self.request.session else None

            if self.cache_dict:
                print('[Memory.show] - CACHE:', self.cache_dict)
            else:
                print('[Memory.show]  Vacio', self.cache_dict)

cache = Memory()

def manage(request):
    return cache.set_request(request)