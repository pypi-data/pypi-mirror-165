# -*- coding: utf-8 -*-
"""
.. module:: main
   :platform: Unix, Windows
   :synopsis: Modelos de uso comun y principal

.. moduleauthor:: Diego Gonzalez <dgonzalez.jim@gmail.com>

"""

from __future__ import unicode_literals

from django.db import models

from . import mixins

class Language(mixins.AuditMixin):
    """

    Language model
    ===================

    Description
        Este modelo permite manejar los lenguajes aceptados en el sistema,
        como version inicial solo permite una codificacion unica. En caso
        de incrementar lenguajes como el Chino Mandarin u similares que
        usen caracteres especiales, se debera crear un campo de codificacion.

    """

    name = models.CharField(max_length=16, null=True, blank=True, unique=True)
    title = models.CharField(max_length=32, null=True, blank=True, unique=True)
    i18n = models.CharField(max_length=5, null=True, blank=True)
    default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """

        Save

        Description
            Sobrecarga el metodo save de model para formatear el nombre (name)

        """
        self.name = self.name.replace(' ','').replace('.','').replace(',','') if self.name else ''
        obj = super(Language, self).save(*args, **kwargs)
        return obj

    def __str__(self):
        return u'%s' % self.name

class Message(mixins.AuditMixin):
    """

    Messages model
    ===================

    Description
        Este modelo permite manejar los mensajes estaticos del sistema
        manteniendolos en base de datos, ademas podra ser almacenado en cache
        para limitar el acceso a base de datos. Si se agrega un cambio a este
        modelo se debera reiniciar el servidor de aplicaciones.


    """

    name = models.CharField(max_length=100, null=True, blank=True, unique=True)
    text = models.TextField(null=True, blank=True)
    published = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        """

        Save

        Description
            Sobrecarga el metodo save de model para formatear el nombre (name)

        """
        self.name = self.name.replace(' ','')
        obj = super(Message, self).save(*args, **kwargs)
        return obj

class MessageTraduction(mixins.AuditMixin):
    """

    Messages Traduction model
    ===================

    Description
        Este modelo permite almacenar la traduccion en otro idioma de un mensaje
        por defecto en caso de que el lenguaje establecido en el portal sea uno
        diferente al lenguaje por defecto (Spanish en mi caso). Si el lenguaje
        seleccionado es el lenguaje por defecto no se extra el texto de este modelo,
        se lo extrae del modelo Message del campo text.

    """
    language = models.ForeignKey('dwll.Language', on_delete=models.PROTECT)
    message = models.ForeignKey('dwll.Message', on_delete=models.PROTECT)
    text = models.TextField(null=True, blank=True)

class Configuration(mixins.AuditMixin):
    """

    Configuration model
    ===================

    Description
        Este modelo permite el almacenamiento de parametros de configuracion
        del sistema. Los parametros son accedidos por el nombre y en el helper
        correspondiente se deben mantener en cache.

    """
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=350, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return u'%s' % self.name
