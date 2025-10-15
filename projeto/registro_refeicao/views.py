from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.db.models import Q

from utils.decorators import LoginRequiredMixin

from .models import RegistroRefeicao

from .forms import BuscaRegistroRefeicaoForm, RegistroRefeicaoForm


class RegistroRefeicaoListView(LoginRequiredMixin, ListView):
    model = RegistroRefeicao
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            #quando ja tem dados filtrando
            context['form'] = BuscaRegistroRefeicaoForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            context['form'] = BuscaRegistroRefeicaoForm()
        return context

    def get_queryset(self):                
        qs = super().get_queryset().all()

        if self.request.GET:
            #quando ja tem dados filtrando
            form = BuscaRegistroRefeicaoForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            form = BuscaRegistroRefeicaoForm()

        if form.is_valid():            
            pesquisa = form.cleaned_data.get('pesquisa')            
                        
            if pesquisa:
                qs = qs.filter(Q(cliente__nome__icontains=pesquisa) | Q(registro_alimentacao__icontains=pesquisa))
            
        return qs


class RegistroRefeicaoCreateView(LoginRequiredMixin, CreateView):
    model = RegistroRefeicao
    # fields = ['cliente', 'registro_alimentacao', 'glicemia_vigente']
    form_class = RegistroRefeicaoForm
    success_url = 'registrorefeicao_list'

    def get_success_url(self):
        messages.success(self.request, 'Registro de refeição cadastrado com sucesso na plataforma!')
        return reverse(self.success_url)


class RegistroRefeicaoUpdateView(LoginRequiredMixin, UpdateView):
    model = RegistroRefeicao
    # fields = ['cliente', 'registro_alimentacao', 'glicemia_vigente']
    form_class = RegistroRefeicaoForm
    success_url = 'registrorefeicao_list'

    def get_success_url(self):
        messages.success(self.request, 'Registro de refeição atualizado com sucesso na plataforma!')
        return reverse(self.success_url)


class RegistroRefeicaoDeleteView(LoginRequiredMixin, DeleteView):
    model = RegistroRefeicao
    success_url = 'registrorefeicao_list'

    def get_success_url(self):
        messages.success(self.request, 'Registro de refeição removido com sucesso na plataforma!')
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
            messages.error(request, 'Há dependências ligadas à esse Registro de refeição, permissão negada!')
        return redirect(self.get_success_url())
    
        
