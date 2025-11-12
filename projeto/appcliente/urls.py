from __future__ import unicode_literals
from django.urls import path

from core.views import HomeRedirectView

from .views import (DadosClienteUpdateView, HomeView, AboutView)

from .views import (MeusDadosClinicosClienteListView, MeusDadosClinicosClienteCreateView,
                    MeusDadosClinicosClienteUpdateView, MeusDadosClinicosClienteDeleteView)


urlpatterns = [
   path('home', HomeView.as_view(), name='appcliente_home'), 
   path('', HomeRedirectView.as_view(), name='home_redirect'),
   path('about', AboutView.as_view(), name='appcliente_about'),

   path('meus-dados/', DadosClienteUpdateView.as_view(), name='appcliente_dados_update'),
   
   path('meus-dados-clinicos-list/', MeusDadosClinicosClienteListView.as_view(), name='appcliente_dadoclinico_list'),
   path('meus-dados-clinicos-cad/', MeusDadosClinicosClienteCreateView.as_view(), name='appcliente_dadoclinico_create'),
   path('meus-dados-clinicos-update/<slug:slug>/', MeusDadosClinicosClienteUpdateView.as_view(), name='appcliente_dadoclinico_update'),
   path('meus-dados-clinicos-delete/<slug:slug>/', MeusDadosClinicosClienteDeleteView.as_view(), name='appcliente_dadoclinico_delete'),
   
   
]
