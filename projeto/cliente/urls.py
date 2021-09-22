from __future__ import unicode_literals
from django.conf.urls import url

from core.views import HomeRedirectView

from .views import (DadosAlunoUpdateView, DocumentoListView, 
                    SubmissaoListView, SubmissaoCreateView, 
                    SubmissaoUpdateView, HomeView, AboutView, AvaliacaoDetailView, 
                    SubmissaoSugestaoPreProjetoDetailView, OrientacaoListView, 
                    OrientacaoCreateView, OrientacaoUpdateView, OrientacaoDetailView)

urlpatterns = [
   url(r'^home$', HomeView.as_view(), name='appaluno_home'), 
   url(r'^$', HomeRedirectView.as_view(), name='home_redirect'),
   url(r'^about$', AboutView.as_view(), name='appaluno_about'),
   url(r'^documentos$', DocumentoListView.as_view(), name='appaluno_documento_list'),

   url(r'^meus-dados/$', DadosAlunoUpdateView.as_view(), name='appaluno_dados_update'),

   url(r'^minhas-submissoes$', SubmissaoListView.as_view(), name='appaluno_submissao_list'),
   url(r'^minhas-submissoes/cad/$', SubmissaoCreateView.as_view(), name='appaluno_submissao_create'),
   url(r'^minhas-submissoes/(?P<pk>\d+)/$', SubmissaoUpdateView.as_view(), name='appaluno_submissao_update'),
   
   url(r'^avaliacao-parecer-liberado/(?P<pk>\d+)/$', AvaliacaoDetailView.as_view(), name='appaluno_avaliacao_parecer_detail'),

   url(r'^sugestao-preprojeto/(?P<pk>\d+)/$', SubmissaoSugestaoPreProjetoDetailView.as_view(), name='appaluno_submissao_sugestao_preprojeto_detail'),
   
   url(r'^minhas-orientacoes/detalhes/(?P<pk>\d+)/$', OrientacaoDetailView.as_view(), name='appaluno_orientacao_detail'),
   url(r'^minhas-orientacoes$', OrientacaoListView.as_view(), name='appaluno_orientacao_list'),
   url(r'^minhas-orientacoes/cad/$', OrientacaoCreateView.as_view(), name='appaluno_orientacao_create'),
   url(r'^minhas-orientacoes/(?P<pk>\d+)/$', OrientacaoUpdateView.as_view(), name='appaluno_orientacao_update'),
   
]
