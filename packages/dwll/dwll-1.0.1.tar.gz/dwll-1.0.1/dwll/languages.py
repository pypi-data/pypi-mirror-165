# -*- coding: utf-8 -*-
"""
.. module:: dbu-messages
   :platform: Unix, Windows
   :synopsis: Manejador de mensajes de uso comun y principal

.. moduleauthor:: Diego Gonzalez <dgonzalez.jim@gmail.com>

"""
from . import models
from .memory import memory

class LanguageManager:
    """

    Language Manager
    ===================

    Description
        Manejador de lenguajes, permite conseguir el lenguaje principal del sistema.

    """

    DEFAULT = 'spanish'

    def get_default(self):
        """
        Return the default language (spanish) 
        :return
            models.Language -- El lenguaje principal del sistema
        """
        main_languages = models.Language.objects.get_active(default=True)

        if main_languages.exists():
            return main_languages.first().name

        name = self.DEFAULT

        models.Language.objects.create(
            name=name,
            title='Espanol',
            i18n='es',
            default=True
        )

        return name

    def get_by_name(self, name):
        """
        Get the language by name
        :return
            models.Language -- El lenguaje
        """
        main_languages = models.Language.objects.get_active(name=name)

        if main_languages.count() > 0:
            return main_languages.first()

        return None

    def get_language(self, request=None):
        """
        Return the selected language or the default language
        :return
            models.Language -- El lenguaje principal del sistema
        """
        if request:
            return memory.manage(request).recover('dbu.languages.current', default_value=self.get_default())

        return self.get_default()


    def get_language_object(self, request):
        """
        Get the object of a language gived the request object, or create by default
        :return
            String -- Abreviacion i18n

        """
        lang_name = self.get_language(request)
        languages = models.Language.objects.get_active(name = lang_name)

        if languages.exists():
            return languages.first()
        else:
            return self.create_language(lang_name)

    def change_language(self, request, name):
        """
        Let to change the language gived the 'name'
        :return
            Boolean -- True if success
        """
        languages = models.Language.objects.get_active(name = name)

        if languages.count() > 0:
            first = languages.first()
            memory.manage(request).store('dbu.languages.current', first.name)
            return True, first

        return False, None

    def create_language(self, name):
        """
        Register a new language or return it if exists
        :param name:
        """
        try:
            return models.Language.objects.create(name = name, title = name)
        except Exception as e:
            languages = models.Language.objects.get_active(name = name)
            if languages.count() > 0:
                return languages.first()

            return None

    def get_languages_list(self, request):
        """
        List of active languages in list format, and with selected one checked
        """
        selected = self.get_language(request)
        return [{'is_selected':selected == lang.name, 'name':lang.name, 'title':lang.title} \
            for lang in models.Language.objects.get_active()]

languages = LanguageManager()