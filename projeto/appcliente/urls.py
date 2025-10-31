from __future__ import unicode_literals
from django.urls import path

from core.views import HomeRedirectView

from .views import (DadosClienteUpdateView, HomeView, AboutView)

urlpatterns = [
   path('home', HomeView.as_view(), name='appcliente_home'), 
   path('', HomeRedirectView.as_view(), name='home_redirect'),
   path('about', AboutView.as_view(), name='appcliente_about'),

   path('meus-dados/', DadosClienteUpdateView.as_view(), name='appcliente_dados_update'),
   
]
