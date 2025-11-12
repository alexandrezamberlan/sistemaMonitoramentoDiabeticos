from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.db.models import Q

from utils.decorators import LoginRequiredMixin

from .models import DadoClinico

from .forms import BuscaDadoClinicoForm, DadoClinicoForm


class DadoClinicoListView(LoginRequiredMixin, ListView):
    model = DadoClinico
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            #quando ja tem dados filtrando
            context['form'] = BuscaDadoClinicoForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            context['form'] = BuscaDadoClinicoForm()
        return context

    def get_queryset(self):                
        qs = super().get_queryset().all()

        if self.request.GET:
            #quando ja tem dados filtrando
            form = BuscaDadoClinicoForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            form = BuscaDadoClinicoForm()

        if form.is_valid():            
            pesquisa = form.cleaned_data.get('pesquisa')            
                        
            if pesquisa:
                qs = qs.filter(Q(cliente__nome__icontains=pesquisa) | Q(medicamentos__nome_comercial__icontains=pesquisa) | Q(medicamentos__principio_ativo__icontains=pesquisa) | Q(medicamentos__classe_terapeutica__icontains=pesquisa) )
            
        return qs


class DadoClinicoCreateView(LoginRequiredMixin, CreateView):
    model = DadoClinico
    # fields = ['cliente', 'medicamentos', 'bolus_alimentar', 'bolus_correcao', 'altura', 'peso', 'is_active']
    form_class = DadoClinicoForm
    success_url = 'dadoclinico_list'

    def get_success_url(self):
        messages.success(self.request, 'Dado clínico cadastrado com sucesso na plataforma!')
        return reverse(self.success_url)


class DadoClinicoUpdateView(LoginRequiredMixin, UpdateView):
    model = DadoClinico
    # fields = ['cliente', 'medicamentos', 'bolus_alimentar', 'bolus_correcao', 'altura', 'peso', 'is_active']
    form_class = DadoClinicoForm
    success_url = 'dadoclinico_list'

    def get_success_url(self):
        messages.success(self.request, 'Dado clínico atualizado com sucesso na plataforma!')
        return reverse(self.success_url)


class DadoClinicoDeleteView(LoginRequiredMixin, DeleteView):
    model = DadoClinico
    success_url = 'dadoclinico_list'

    def get_success_url(self):
        messages.success(self.request, 'Dado clínico removido com sucesso na plataforma!')
        return reverse(self.success_url)

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL. If the object is protected, send an error message.
        """
        self.object = self.get_object()
        try:
            self.object.delete()
        except Exception as e:
            messages.error(request, 'Há dependências ligadas à esse Exercício, permissão negada!')
        return redirect(self.get_success_url())
    
        
