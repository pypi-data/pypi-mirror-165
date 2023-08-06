
from import_export.admin import ImportExportModelAdmin

from .modeladmin import ModelAdminMixin

class ImportExportModelAdminMixin(ImportExportModelAdmin, ModelAdminMixin):
    """

    Import Export Model
    Admin Mixin
    ===================

    Description
        Esta clase permite manejar un manager comun para todos los administradores
        de modelos del sistema que tengan posibilidad de Import Export

    """
    pass