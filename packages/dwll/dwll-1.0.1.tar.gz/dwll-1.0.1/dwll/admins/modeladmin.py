from django.contrib import admin

from . import base

class ModelAdminMixin(admin.ModelAdmin, base.AdminMixinBase):
    """

    Model Admin Mixin
    ===================

    Description
        Esta clase permite manejar un manager comun para todos los administradores
        de modelos del sistema, tiene las funciones basicas de un ModelAdmin sobrecargadas.

    """

    def get_urls(self):
        """

        Get URLS

        Description
            Devuelve la lista de URLs de este Administrador

        """
       
        urls = super(ModelAdminMixin, self).get_urls()

        methods = self.get_dual_methods(self.obj if hasattr(self, 'obj') else None)

        custom_urls = []

        for m in methods:
            try:
                from django.conf.urls import url
                custom_urls.append(
                    url(r'(?P<id>\d+)/%s/$' % m['name'], self.admin_site.admin_view(m['function_view'])),
                )
            except:
                from django.urls import include, re_path
                custom_urls.append(
                    re_path(r'(?P<id>\d+)/{}/$'.format(m['name']), include(self.admin_site.admin_view(m['function_view']))),
                )
            

        return custom_urls + urls

    def get_list_display(self, request):
        """

        Get List Display

        Description
            Override

        """
        if not self.has_this_permission(request):
            self.list_display_links = (None, )

            if hasattr(self, 'protected_links') and not request.user.is_superuser:
                self.list_display = list(self.list_display)

                try:
                    for pl in self.protected_links:
                        self.list_display.remove(pl)
                except:
                    pass

                self.list_display = tuple(self.list_display)
        else:
            if hasattr(self, 'original_list_display'):
                self.list_display = self.original_list_display
                self.list_display_links = ('id', )

        return super(ModelAdminMixin, self).get_list_display(request)