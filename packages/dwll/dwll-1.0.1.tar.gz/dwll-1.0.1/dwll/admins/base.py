
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.contrib import messages

from dwll import messages as __
from . import constants as C

class AdminMixinBase:

    """

    Model Admin Mixin
    ===================

    Description
        Esta clase permite manejar un manager comun para todos los administradores
        de modelos del sistema, tiene las funciones basicas de un ModelAdmin sobrecargadas.

    """

    def get_form(self, request, obj=None, **kwargs):
        """

        Get Form

        Description
            Sobrecarga del metodo get_form de ModelAdmin para excluir de los usuarios
            NO super usuarios, los campos de auditoria

        :param request:
        :param obj:
        :param kwargs:
        :return:
        """
        if not request.user.is_superuser:
            self.exclude = ['status', 'creation_date', 'creation_user', 'modification_date', 'modification_user']
        return super(AdminMixinBase, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        """

        Save Model

        Description
            Sobrecarga del metodo save_model de ModelAdmin para almacenar el usaurio que
            esta realizando una afectacion a un modelo desde el Admin Django.

        :param request:
        :param obj:
        :param form:
        :param change:
        :return:
        """
        obj.save(request = request)

    def get_dual_methods(self, obj=None, disable_color=C.DISABLED_COLOR, enable_color=C.ENABLED_COLOR):
        """

        Get Dual Methods

        Description
            Devuelve los metodos duales que se aplican en el administrador de este modelo

        :return:
        """

        if not hasattr(self, 'obj'):
            self.obj = obj
        else:
            obj = self.obj

        enable_disable_methods = [
            {'name':'enable', 'activation': True, 'color':disable_color, 'function_view':self.enable_view},
            {'name':'disable', 'activation': True, 'color':enable_color, 'function_view':self.disable_view},
        ]

        if hasattr(self, 'get_specific_dual_methods'):
            return self.get_specific_dual_methods(obj) + enable_disable_methods
        else:
            return enable_disable_methods

    def get_url(self):
        """

        Get URL

        Description
            Devuelve la URL relativa de este proceso

        :return:
        """
        info = self.model._meta.app_label, self.model._meta.model_name
        return '/admin/%s/%s/' % info

    def extra_actions(self, obj, separator=C.LINKS_SEPARATOR):
        """

        Get Status Change

        Description
            Devuelve un link para cambiar el estado de Activo
            a Inactivo o visceversa.

        """

        links = []

        for method in self.get_dual_methods(obj):

            if 'activation' in method and method['activation']:

                message = self.get_message(method['name'],'confirm')
                url = self.get_url() + '%d/%s/' % (obj.id, method['name'])
                label = self.get_message(method['name'],'label')
                color = method['color']

                link = '<a href="#" onclick="var r = confirm(\'%s\'); if (r == true){ ' \
                       'window.location.replace(\'%s\');}" ' \
                       'style="color:%s">%s</a>' % (message, url, color, label)

            if 'enquire' in method and method['enquire']:

                message = self.get_message(method['name'],'enquire')
                url = self.get_url() + '%d/%s/' % (obj.id, method['name'])
                label = self.get_message(method['name'],'label')
                color = method['color']

                default_value = ''
                if 'field_value' in method and method['field_value']:
                    default_value = getattr(obj, method['field_value'])

                link = '<a href="#" onclick="var r = prompt(\'%s\', \'%s\'); if (r != null){ ' \
                       'window.location.replace(\'%s?c=\'+r);}" ' \
                       'style="color:%s">%s</a>' % (message, default_value, url, color, label)

            links.append(link)


        return mark_safe(separator.join(links))

    # Configura el link para mostrarse en la columna
    extra_actions.short_description = 'Actions'

    def change_boolean_value_view(self, request, id, field_name):
        """

        Cambia el valor booleano de un campo

        :param request:
        :param id:
        :param field_name:
        :return:
        """
        try:

            obj = self.get_object(request, id)

            field = getattr(obj, field_name)

            if field is None:
                setattr(obj, field_name, True)
            else:
                setattr(obj, field_name, not field)

            obj.username = request.user.username
            obj.save()
            msg = '{} {}'.format(__.get_message('admin.action.%s.success' % field_name), obj.id)
            return self.response_view(request, True, '%s_view' % field_name, msg)
        except Exception as e:
            return self.response_view(request, False, '%s_view' % field_name, 'Error: {}'.format(str(e)))

    def enable_view(self, request, id):
        """

        Enable View

        Description
            Vista para habilitar una entidad

        :return:
        """
        try:
            obj = self.get_object(request, id)
            obj.enable(request.user.username)
            success_msg = __.get_message('admin.enable.success')
            return self.response_view(request, True, 'enable_view', '{}: {}'.format(success_msg, obj.id))
        except Exception as e:
            return self.response_view(request, False, 'enable_view', 'Error: {}'.format(str(e)))

    def disable_view(self, request, id):
        """

        Disable View

        Description
            Vista para deshabilitar una entidad

        :return:
        """
        try:
            obj = self.get_object(request, id)
            obj.disable(request.user.username)
            success_msg = __.get_message('admin.disable.success')
            return self.response_view(request, True, 'disable_view', '{}: {}'.format(success_msg, obj.id))
        except Exception as e:
            return self.response_view(request, False, 'disable_view', 'Error: {}'.format(str(e)))

    def response_view(self, request, response, method, extra_msg=''):
        """

        Response View

        Description
            Devuelve un HTTP Response Redirect luego de escribir un mensaje en pantalla

        :param request:
        :param response:
        :param method:
        :param extra_msg:
        :return:
        """
        if response:
            self.show_success_message(request, method, extra_msg)
        else:
            self.show_error_message(request, method, extra_msg)

        return HttpResponseRedirect(self.get_url())

    def show_success_message(self, request, method, extra_msg=''):
        """

        Show Success Message

        Description
            Muestra en pantalla el resultado de una ejecucion exitosa

        :param request:
        :param method:
        :return:
        """
        messages.info(request, '%s %s' % (self.get_message(method, 'success'), extra_msg) )

    def show_error_message(self, request, method, extra_msg=''):
        """

        Show Error Message

        Description
            Muestra en pantalla el resultado de una ejecucion fallida

        :param request:
        :param method:
        :return:
        """
        messages.error(request, '%s %s' % (self.get_message(method, 'fail'), extra_msg) )

    def get_message(self, method, response):
        """

        Get Message

        Description
            Metodo sobreescribible para obtener un mensaje

        """

        if hasattr(self, 'get_specific_message'):
            return self.get_specific_message(method, response)
        else:
            return __.get_message('admin.%s.entity.%s' % (method, response))

    def has_this_permission(self, request):
        """

        Has This Permission

        Description
            Verifica si tiene un permiso especifico

        """
        return True