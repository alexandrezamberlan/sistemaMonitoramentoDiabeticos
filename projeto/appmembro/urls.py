from __future__ import unicode_literals
from django.urls import path

from core.views import HomeRedirectView

from .views import (DadosMembroUpdateView, HomeView, AboutView)

urlpatterns = [
   path('home', HomeView.as_view(), name='appmembro_home'), 
   path('', HomeRedirectView.as_view(), name='home_redirect'),
   path('about', AboutView.as_view(), name='appmembro_about'),

   path('meus-dados/', DadosMembroUpdateView.as_view(), name='appmembro_dados_update'),
   
]
