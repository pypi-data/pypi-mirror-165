# -*- coding: utf-8 -*-
"""
.. module:: dwll
   :platform: Unix, Windows
   :synopsis: URLS para modulo principal

.. moduleauthor:: Diego Gonzalez <dgonzalez.jim@gmail.com>

"""
from django.urls import path, include

from . import views

urlpatterns = [

    # Standard Views
    path('language/<name>/', views.change_language, name='change-language'),
    
]
