# -*- coding: utf-8 -*-
"""
.. module:: dbu-admin
   :platform: Unix, Windows
   :synopsis: Administrador de Modelos de modulo dbu

.. moduleauthor:: Diego Gonzalez <dgonzalez.jim@gmail.com>

"""
from django.contrib import admin

from .models import Language, MessageTraduction, Message, Configuration

#from .admins import modeladmin

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):#modeladmin.ModelAdminMixin
    list_display = ('id', 'name', 'default', 'modification_date', 'modification_user')

@admin.register(MessageTraduction)
class MessageTraductionAdmin(admin.ModelAdmin):#modeladmin.ModelAdminMixin
    #resource_class = impexp.MessageTraductionResource
    list_display = ('id', 'language', 'message', 'modification_date', 'modification_user')

class MessageTraductionAdminTabular(admin.TabularInline):
    model = MessageTraduction
    extra = 0
    max_num = 10
    exclude = ('status', 'creation_date', 'creation_user', 'modification_date', 'modification_user')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):#modeladmin.ModelAdminMixin
    inlines = [MessageTraductionAdminTabular, ]
    #resource_class = impexp.MessageResource
    list_display = ('id', 'name', 'text', 'published', 'modification_date', 'modification_user')
    search_fields = ['name','text']
    list_filter = ['modification_date','creation_date']

@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):#modeladmin.ModelAdminMixin
    #resource_class = impexp.ConfigurationResource
    list_display = ('id', 'name', 'value', 'description', 'modification_date', 'modification_user')
    search_fields = ['name','value','description']
