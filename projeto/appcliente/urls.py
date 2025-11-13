from __future__ import unicode_literals
from django.urls import path

from core.views import HomeRedirectView

from .views import (DadosClienteUpdateView, HomeView, AboutView)

from .views import (MeusDadosClinicosClienteListView, MeusDadosClinicosClienteCreateView,
                    MeusDadosClinicosClienteUpdateView, MeusDadosClinicosClienteDeleteView)

from .views import (MinhaRefeicaoListView, MinhaRefeicaoCreateView, MinhaRefeicaoDeleteView)

from .views import (MeuRegistroAtividadeListView, MeuRegistroAtividadeCreateView,
                    MeuRegistroAtividadeUpdateView, MeuRegistroAtividadeDeleteView)

urlpatterns = [
   path('home', HomeView.as_view(), name='appcliente_home'), 
   path('', HomeRedirectView.as_view(), name='home_redirect'),
   path('about', AboutView.as_view(), name='appcliente_about'),

   path('meus-dados/', DadosClienteUpdateView.as_view(), name='appcliente_dados_update'),
   
   path('meus-dados-clinicos-list/', MeusDadosClinicosClienteListView.as_view(), name='appcliente_dadoclinico_list'),
   path('meus-dados-clinicos-cad/', MeusDadosClinicosClienteCreateView.as_view(), name='appcliente_dadoclinico_create'),
   path('meus-dados-clinicos-update/<slug:slug>/', MeusDadosClinicosClienteUpdateView.as_view(), name='appcliente_dadoclinico_update'),
   path('meus-dados-clinicos-delete/<slug:slug>/', MeusDadosClinicosClienteDeleteView.as_view(), name='appcliente_dadoclinico_delete'),

   path('minhas-refeicoes-list/', MinhaRefeicaoListView.as_view(), name='appcliente_registrorefeicao_list'),
   path('minhas-refeicoes-cad/', MinhaRefeicaoCreateView.as_view(), name='appcliente_registrorefeicao_create'),
   #path('minhas-refeicoes-update/<slug:slug>/', MinhaRefeicaoUpdateView.as_view(), name='appcliente_registrorefeicao_update'),
   path('minhas-refeicoes-delete/<slug:slug>/', MinhaRefeicaoDeleteView.as_view(), name='appcliente_registrorefeicao_delete'),
   
   path('minhas-atividades-list/', MeuRegistroAtividadeListView.as_view(), name='appcliente_registroatividade_list'),
   path('minhas-atividades-cad/', MeuRegistroAtividadeCreateView.as_view(), name='appcliente_registroatividade_create'),
   path('minhas-atividades-update/<slug:slug>/', MeuRegistroAtividadeUpdateView.as_view(), name='appcliente_registroatividade_update'),
   path('minhas-atividades-delete/<slug:slug>/', MeuRegistroAtividadeDeleteView.as_view(), name='appcliente_registroatividade_delete'),
   
]
