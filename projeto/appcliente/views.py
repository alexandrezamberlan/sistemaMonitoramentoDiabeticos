from __future__ import unicode_literals

import locale

from itertools import chain
from operator import attrgetter

from django.contrib.staticfiles import finders

from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView

from django.http import HttpResponse
from django.template.loader import render_to_string

from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.units import inch
from reportlab.lib import colors

from mail_templated import EmailMessage

from utils.decorators import LoginRequiredMixin, ClienteRequiredMixin


from aviso.models import Aviso



from usuario.models import Usuario

from .forms import ClienteCreateForm



class HomeView(LoginRequiredMixin, ClienteRequiredMixin, TemplateView):
    template_name = 'appcliente/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['avisos'] = Aviso.ativos.filter(destinatario__in=[self.request.user.tipo, 'TODOS'])[0:2]
        return context

class AboutView(LoginRequiredMixin, ClienteRequiredMixin, TemplateView):
    template_name = 'appcliente/about.html'
    

class DadosClienteUpdateView(LoginRequiredMixin, ClienteRequiredMixin ,UpdateView):
    model = Usuario
    template_name = 'appcliente/dados_cliente_form.html'
    form_class = ClienteCreateForm  
    
    success_url = 'appcliente_home'

    def get_object(self, queryset=None):
        return self.request.user
     
    def get_success_url(self):
        messages.success(self.request, 'Seus dados foram alterados com sucesso!')
        return reverse(self.success_url)
    

