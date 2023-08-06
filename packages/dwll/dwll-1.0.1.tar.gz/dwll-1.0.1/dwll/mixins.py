# -*- coding: utf-8 -*-
"""
.. module:: main
   :platform: Unix, Windows
   :synopsis: Mixins de uso principal y comun

.. moduleauthor:: Diego Gonzalez <dgonzalez.jim@gmail.com>

"""
from django.db import models
from django.utils import timezone

from django.db import transaction, IntegrityError

from . import properties

import traceback
import uuid

class CommonManager(models.Manager):
    """

    Common Manager
    ===================

    Description
        Esta clase permite manejar un manager comun para todos los modelos
        que extiendan de Audit Mixin y extraer consultas comunes.

    """

    def get_active(self, *args, **kwargs):
        """

        Get Active

        """
        filtered = self.get_queryset().filter(*args, **kwargs)
        filtered = filtered.filter(status=AuditMixin.ACTIVE)
        return filtered

    def get_enabled(self, *args, **kwargs):
        """

        Get First Enabled

        """
        try:
            elements = self.get_active(*args, **kwargs)
            if elements.count() > 0:
                return elements[0]
        except Exception as e:
            traceback.print_exc()

        return None

class AuditMixin(models.Model):
    """

    Audit Mixin
    ===================

    Description
        Esta clase permite manejar un modelos con campos comunes
        usados para auditoria y control de existencia.

    """

    ACTIVE = properties.ACTIVE
    INACTIVE = properties.INACTIVE

    ESTADO_CHOICES = (
        (ACTIVE, 'Activo'),
        (INACTIVE, 'Inactivo'),
    )

    status = models.CharField(max_length=1, choices=ESTADO_CHOICES, default=ACTIVE)
    creation_user = models.CharField(max_length=64, null=True, blank=True)
    modification_user = models.CharField(max_length=64, null=True, blank=True)
    creation_date = models.DateTimeField(null=True, blank=True)
    modification_date = models.DateTimeField(null=True, blank=True)

    objects = CommonManager()

    def __init__(self, *args, **kwargs):
        """

        INIT

        :param args:
        :param kwargs:
        :return:
        """
        self.username = None
        super(AuditMixin, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        """

        Save

        Description
            Save Overload

        :param args:
        :param kwargs:
        :return:
        """
        request = kwargs.pop('request', None)
        user = request.user if request else None

        if not self.status:
            self.status = self.ACTIVE

        if not self.creation_user and user:
            self.creation_user = user.username[:64] if user else None

        if not self.creation_date:
            self.creation_date = timezone.now()

        self.modification_date = timezone.now()

        self.modification_user = user.username[:64] if user else self.modification_user

        obj = super(AuditMixin, self).save(*args, **kwargs)
        return obj

    def is_enabled(self):
        """

        Is Enabled

        Description
            Reg is Available

        :return:
        """
        return self.status == self.ACTIVE

    def disable(self, user=None):
        """

        Disable

        Description
            Disable a reg

        :param user:
        :return:
        """
        self.status = self.INACTIVE
        self.modification_user = user[:64] if user else ''
        self.save()

    def enable(self, user=None):
        """

        Enable

        Description
            Enable a reg

        :param user:
        :return:
        """
        self.status = self.ACTIVE
        self.modification_user = user[:64] if user else ''
        self.save()

    def get_creation_date(self):
        """

        Get Creation Time

        Description
            Get Creation Time Formated

        :return:
        """
        try:
            return self.creation_date.strftime('%d/%m/%Y %H:%M:%S')
        except:
            return str(self.creation_date)

    def get_modification_date(self):
        """

        Get Modification Time

        Description
            Get Modification Time Formated

        :return:
        """
        try:
            return self.modification_date.strftime('%d/%m/%Y %H:%M:%S')
        except:
            return str(self.modification_date)

    class Meta:
        abstract = True

class AuditMixinCode(AuditMixin):
    """

    Audit Mixin Code
    ===================

    Description
        Esta clase permite manejar un modelos con campos estandares mas un codigo alfanumerico

    """

    code = models.CharField(max_length=12, null=True, blank=True, unique=True)

    def save(self, *args, **kwargs):
        """

        Save Entity

        Description
            Guarda con codigo especial unico de entidad,
            garantizamos que sea unico

        :param args:
        :param kwargs:
        :return:
        """

        if not self.code:

            max_tries = 50
            while True:
                if max_tries > 0:
                    try:
                        self.code = self.generate_unique_id_12()
                        savepoint = transaction.savepoint()
                        super(AuditMixinCode, self).save(*args, **kwargs)
                        transaction.savepoint_commit(savepoint)
                        break
                    except IntegrityError as e:
                        print('<- [AuditMixinCode.save] Error al guardar: %s' % str(e))
                        transaction.savepoint_rollback(savepoint)
                    max_tries -= 1
                else:
                    print('<- [AuditMixinCode.save] No se pudo generar ID UNICO')
                    break
        else:
            super(AuditMixinCode, self).save(*args, **kwargs)

    @staticmethod
    def get_unique_code(max=12):
        """

        Get Unique Code

        Description
            Metodo estatico para generar codigos Unicos

        :return:
        """
        uid = uuid.uuid4().int & (1 << 64) - 1
        return str(uid)[:max]

    def generate_unique_id_12(self):
        """

        Generates Unique ID 12

        Description
            Generates a Unique ID of 12 digits

        :return:
        """
        return AuditMixinCode.get_unique_code()

    class Meta:
        abstract = True