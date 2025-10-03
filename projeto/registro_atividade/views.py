from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.db.models import Q

from utils.decorators import LoginRequiredMixin

from .models import RegistroAtividade

from .forms import BuscaRegistroAtividadeForm


class RegistroAtividadeListView(LoginRequiredMixin, ListView):
    model = RegistroAtividade
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            #quando ja tem dados filtrando
            context['form'] = BuscaRegistroAtividadeForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            context['form'] = BuscaRegistroAtividadeForm()
        return context

    def get_queryset(self):                
        qs = super().get_queryset().all()

        if self.request.GET:
            #quando ja tem dados filtrando
            form = BuscaRegistroAtividadeForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            form = BuscaRegistroAtividadeForm()

        if form.is_valid():            
            pesquisa = form.cleaned_data.get('pesquisa')            
                        
            if pesquisa:
                qs = qs.filter(Q(cliente__nome__icontains=pesquisa) | Q(atividade__nome__icontains=pesquisa))
            
        return qs


class RegistroAtividadeCreateView(LoginRequiredMixin, CreateView):
    model = RegistroAtividade
    fields = ['cliente', 'data', 'hora', 'atividade', 'duracao', 'esforco', 'frequencia_cardiaca_media']
    success_url = 'registroatividade_list'

    def get_success_url(self):
        messages.success(self.request, 'Registro de atividade cadastrado com sucesso na plataforma!')
        return reverse(self.success_url)


class RegistroAtividadeUpdateView(LoginRequiredMixin, UpdateView):
    model = RegistroAtividade
    fields = ['cliente', 'data', 'hora', 'atividade', 'duracao', 'esforco', 'frequencia_cardiaca_media']
    success_url = 'registroatividade_list'

    def get_success_url(self):
        messages.success(self.request, 'Registro de atividade atualizado com sucesso na plataforma!')
        return reverse(self.success_url)


class RegistroAtividadeDeleteView(LoginRequiredMixin, DeleteView):
    model = RegistroAtividade
    success_url = 'registroatividade_list'

    def get_success_url(self):
        messages.success(self.request, 'Registro de atividade removido com sucesso na plataforma!')
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
    
        
