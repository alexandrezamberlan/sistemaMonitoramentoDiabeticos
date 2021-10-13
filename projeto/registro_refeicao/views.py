from __future__ import unicode_literals

from django.contrib import messages
from django.http import Http404, JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from utils.decorators import LoginRequiredMixin, StaffRequiredMixin

from .models import RegistroRefeicao


class RegistroRefeicaoListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = RegistroRefeicao
    template_name = 'registro_refeicao/registro_refeicao_list.html'

class RegistroRefeicaoCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
	model = RegistroRefeicao
	template_name = 'registro_refeicao/registro_refeicao_form.html'
	fields = ['data', 'hora', 'alimento', 'quantidade']
	success_url = 'registro_refeicao_list'

	def get_success_url(self):
		messages.success(self.request, 'Registro da refeição cadastrado com sucesso!!')
		return reverse(self.success_url)

class RegistroRefeicaoUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
	model = RegistroRefeicao
	template_name = 'registro_refeicao/registro_refeicao_form.html'
	fields = ['data', 'hora', 'alimento', 'quantidade']
	success_url = 'registro_refeicao_list'
 
	def get_success_url(self):
		messages.success(self.request, 'Registro da refeição atualizado com sucesso!!')
		return reverse(self.success_url)


class RegistroRefeicaoDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = RegistroRefeicao
    template_name = 'registro_refeicao/registro_refeicao_confirm_delete.html'
    success_url = 'registro_refeicao_list'
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()		
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.success(request, 'Registro de refeição excluído com sucesso!') 
        except Exception as e:
            messages.error(request, 'Há dependências ligadas a esse registro, permissão negada!')
        return redirect(self.success_url)