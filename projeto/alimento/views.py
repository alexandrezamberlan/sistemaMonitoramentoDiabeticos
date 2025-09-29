from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.db.models import Q

from utils.decorators import LoginRequiredMixin

from .models import Alimento

from .forms import BuscaAlimentoForm


class AlimentoListView(LoginRequiredMixin, ListView):
    model = Alimento
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            #quando ja tem dados filtrando
            context['form'] = BuscaAlimentoForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            context['form'] = BuscaAlimentoForm()
        return context

    def get_queryset(self):                
        qs = super().get_queryset().all()

        if self.request.GET:
            #quando ja tem dados filtrando
            form = BuscaAlimentoForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            form = BuscaAlimentoForm()

        if form.is_valid():            
            pesquisa = form.cleaned_data.get('pesquisa')            
                        
            if pesquisa:
                qs = qs.filter(Q(descricao__icontains=pesquisa) | Q(unidade__icontains=pesquisa) | Q(fonte__icontains=pesquisa))
            
        return qs


class AlimentoCreateView(LoginRequiredMixin, CreateView):
    model = Alimento
    fields = ['descricao', 'unidade', 'calorias', 'carboidratos', 'fonte']
    success_url = 'alimento_list'

    def get_success_url(self):
        messages.success(self.request, 'Alimento cadastrado com sucesso na plataforma!')
        return reverse(self.success_url)


class AlimentoUpdateView(LoginRequiredMixin, UpdateView):
    model = Alimento
    fields = ['descricao', 'unidade', 'calorias', 'carboidratos', 'fonte']
    success_url = 'alimento_list'

    def get_success_url(self):
        messages.success(self.request, 'Alimento atualizado com sucesso na plataforma!')
        return reverse(self.success_url)


class AlimentoDeleteView(LoginRequiredMixin, DeleteView):
    model = Alimento
    success_url = 'alimento_list'

    def get_success_url(self):
        messages.success(self.request, 'Alimento removido com sucesso na plataforma!')
        return reverse(self.success_url)

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL. If the object is protected, send an error message.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.delete()
        except Exception as e:
            messages.error(request, 'Há dependências ligadas à esse Alimento, permissão negada!')
        return redirect(self.success_url)
    
        
