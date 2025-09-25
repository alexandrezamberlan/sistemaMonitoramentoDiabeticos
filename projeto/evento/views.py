from __future__ import unicode_literals

from django.contrib import messages

from django.db.models import Q

from django.shortcuts import redirect

from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse

from utils.decorators import LoginRequiredMixin, StaffRequiredMixin, CoordenadorRequiredMixin

from .models import Evento

from .forms import BuscaEventoForm, EventoForm, EventoCoordenadorForm


class EventoListView(LoginRequiredMixin, CoordenadorRequiredMixin, ListView):
    model = Evento

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            #quando ja tem dados filtrando
            context['form'] = BuscaEventoForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            context['form'] = BuscaEventoForm()
        return context

    def get_queryset(self):                
        if self.request.user.tipo == 'ADMINISTRADOR':
            qs = super().get_queryset().all()        

        if self.request.user.tipo == 'COORDENADOR' or self.request.user.tipo == 'MINISTRANTE':
            qs = super().get_queryset().all()
            qs = qs.filter(coordenador=self.request.user)

        if self.request.GET:
            #quando ja tem dados filtrando
            form = BuscaEventoForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            form = BuscaEventoForm()

        if form.is_valid():            
            pesquisa = form.cleaned_data.get('pesquisa')            
                        
            if pesquisa:
                qs = qs.filter(Q(coordenador__nome__icontains=pesquisa) | Q(nome__icontains=pesquisa) | Q(descricao__icontains=pesquisa) | 
                               Q(tipo__descricao__icontains=pesquisa) | Q(local__icontains=pesquisa) | Q(instituicao__nome__icontains=pesquisa))
            
        return qs
 

class EventoCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Evento
    form_class = EventoForm
    success_url = 'evento_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Evento cadastrado com sucesso na plataforma!')
        return reverse(self.success_url)

    def form_valid(self, form):
        formulario = form.save(commit=False)
        
        if formulario.data_inscricao > formulario.data_inicio:
            messages.error(self.request,"Data de inscrição deve ser menor ou igual a data do evento!")  
            return super().form_invalid(form)
        
        formulario.save()

        return super().form_valid(form)   


class EventoUpdateView(LoginRequiredMixin, CoordenadorRequiredMixin, UpdateView):
    model = Evento
    form_class = EventoForm
    success_url = 'evento_list'
    
    def get_form_class(self):
        if self.request.user.tipo == 'COORDENADOR':
            return EventoCoordenadorForm
        return super().get_form_class()

    def get_template_names(self):
        if self.request.user.tipo == 'COORDENADOR':
            return 'evento/evento_coordenador_form.html'
        return super().get_template_names()

    def get_success_url(self):
        messages.success(self.request, 'Evento atualizado com sucesso na plataforma!')
        return reverse(self.success_url) 


class EventoDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Evento
    success_url = 'evento_list'

    def get_success_url(self):
        messages.success(self.request, 'Evento removido com sucesso da plataforma!')
        return reverse(self.success_url) 

    def post(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL. If the object is protected, send an error message.
        """
        try:
            self.object = self.get_object()
            self.object.delete()
        except Exception as e:
            messages.error(request, 'Há dependências ligadas à esse Evento, permissão negada!')
        return redirect(self.success_url)