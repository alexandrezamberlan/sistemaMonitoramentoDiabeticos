from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login

from django.db.models import Q

from django.shortcuts import redirect
from django.urls import reverse

from django.views.generic import ListView, TemplateView, DetailView, RedirectView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from mail_templated import EmailMessage

from utils.decorators import LoginRequiredMixin, StaffRequiredMixin, CoordenadorRequiredMixin

from .models import Usuario
from .forms import BuscaUsuarioForm
from .forms import UsuarioRegisterForm


class UsuarioListView(LoginRequiredMixin, CoordenadorRequiredMixin, ListView):
    model = Usuario

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            #quando ja tem dados filtrando
            context['form'] = BuscaUsuarioForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            context['form'] = BuscaUsuarioForm()
        return context

    def get_queryset(self):                
        if (not self.request.user.tipo == 'ADMINISTRADOR'):
            qs = super().get_queryset().exclude(tipo = 'ADMINISTRADOR')
        else:
            qs = super().get_queryset().all()
        
        if self.request.GET:
            #quando ja tem dados filtrando
            form = BuscaUsuarioForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            form = BuscaUsuarioForm()

        if form.is_valid():            
            pesquisa = form.cleaned_data.get('pesquisa')
                       
            if pesquisa:
                qs = qs.filter(Q(nome__icontains=pesquisa) | Q(email__icontains=pesquisa) | Q(celular__icontains=pesquisa) | Q(cpf__icontains=pesquisa) | Q(data_nascimento__icontains=pesquisa) | Q(sexo__icontains=pesquisa))
            
        return qs


class UsuarioCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Usuario
    fields = ['tipo', 'nome', 'data_nascimento', 'sexo', 'celular', 'cpf', 'email', 'password', 'aceita_termo', 'is_active']
    success_url = 'usuario_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Usuário cadastrado com sucesso na plataforma!')
        return reverse(self.success_url)


class UsuarioUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Usuario
    fields = ['tipo', 'nome', 'data_nascimento', 'sexo', 'celular', 'cpf', 'email', 'is_active']
    success_url = 'usuario_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Dados do usuário atualizados com sucesso na plataforma!')
        return reverse(self.success_url)


class UsuarioDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Usuario
    success_url = 'usuario_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Usuário removido com sucesso da plataforma!')
        return reverse(self.success_url)


    def post(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL. If the object is protected, send an error message.
        """        
        try:
            self.get_object().delete()
        except Exception as e:
            messages.error(request, f'Há dependências ligadas a esse Usuário, permissão negada!')
        return redirect(self.success_url)


class UsuarioRegisterView(CreateView):
    model = Usuario
    form_class = UsuarioRegisterForm
    template_name = 'usuario/usuario_register_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        
        return super(UsuarioRegisterView, self).form_valid(form)
    
    def get_success_url(self):
        try:
            message = EmailMessage('usuario/email/validacao_email.html', {'usuario': self.object}, settings.EMAIL_HOST_USER, to=[self.object.email])
            message.send()
            return reverse('usuario_register_success') 
        except:
            return reverse('usuario_register_success_falha_email') 
        

class UsuarioRegisterSuccessView(TemplateView):
    template_name= 'usuario/usuario_register_success.html'


class UsuarioRegisterSuccessFalhaEmailView(TemplateView):
    template_name= 'usuario/usuario_register_success_falha_email.html'


class UsuarioRegisterActivateView(RedirectView):
    models = Usuario

    def get_redirect_url(self, *args, **kwargs):
        self.object = Usuario.objects.get(slug=kwargs.get('slug'))
        self.object.is_active = True
        self.object.save()
        login(self.request, self.object)
        messages.success(self.request, 'Obrigado por acessar o Sistema Online de Monitoramento da Diabetes - SOMDiabetes. Esta é a sua área restrita.')
        return reverse('appmembro_home')