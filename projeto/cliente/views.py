from __future__ import unicode_literals
import os
from datetime import datetime
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from django.views.generic import ListView, RedirectView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView

from mail_templated import EmailMessage

from utils.decorators import LoginRequiredMixin, AlunoRequiredMixin

from avaliacao.models import Avaliacao
from documento.models import Documento
from orientacao.models import Orientacao
from submissao.models import Submissao
from usuario.models import Usuario

from .forms import SubmissaoForm

class DocumentoListView(LoginRequiredMixin, AlunoRequiredMixin, ListView):
    model = Documento
    template_name = 'appaluno/documento_list.html'
    
    # def get_queryset(self):
    #     queryset = super(DocumentoListView, self).get_queryset()
    #     return queryset.filter(aluno = self.request.user)


class HomeRedirectView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, **kwargs):
        if self.request.user.tipo == 'ADMINISTRADOR':
            return reverse('home')
        elif self.request.user.tipo == 'ALUNO':
            return reverse('appaluno_home')
        elif self.request.user.tipo == 'AVALIADOR CONVIDADO':
            return reverse('appprofessor_home')
        elif self.request.user.tipo == 'COORDENADOR':
            return reverse('home')
        elif self.request.user.tipo == 'PROFESSOR':
            return reverse('appprofessor_home')
        elif self.request.user.tipo == 'SECRETÁRIA':
            return reverse('home')


class HomeView(LoginRequiredMixin, AlunoRequiredMixin, TemplateView):
    template_name = 'appaluno/home.html'


class AboutView(LoginRequiredMixin, AlunoRequiredMixin, TemplateView):
    template_name = 'appaluno/about.html'
    

class DadosAlunoUpdateView(LoginRequiredMixin, AlunoRequiredMixin, UpdateView):
    model = Usuario
    template_name = 'appaluno/dados_aluno_form.html'
    fields = ['nome','matricula','curso','cpf', 'fone']
    success_url = 'appaluno_home'

    def get_object(self, queryset=None):
        return self.request.user
     
    def get_success_url(self):
        messages.success(self.request, 'Seus dados foram alterados com sucesso!')
        return reverse(self.success_url)


class SubmissaoListView(LoginRequiredMixin, AlunoRequiredMixin, ListView):
    model = Submissao
    template_name = 'appaluno/submissao_list.html'
   
    def get_queryset(self):
        queryset = super(SubmissaoListView, self).get_queryset()
        return queryset.filter(aluno = self.request.user)


class SubmissaoCreateView(LoginRequiredMixin, AlunoRequiredMixin, CreateView):
    model = Submissao
    template_name = 'appaluno/submissao_form.html'
    form_class = SubmissaoForm
    success_url = 'appaluno_submissao_list'
    
    def get_initial(self):
        initials = super().get_initial()
        initials['usuario'] = Usuario.objects.get(id=self.request.GET.get('usuario_id'))
        return initials
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['aluno'] = Usuario.objects.get(id=self.request.GET.get('usuario_id'))
        return context

    def form_valid(self, form):
        try:
            submissao = form.save(commit=False)
            submissao.aluno = Usuario.objects.get(id=self.request.GET.get('usuario_id'))
            submissao.save()
        except Exception as e:
            messages.error(self.request, 'Erro ao submeter o projeto. %s' % e)
        
        return super().form_valid(form)
        # return super(SubmissaoCreateView, self).form_valid(form)
    
    def get_success_url(self):
        messages.success(self.request, 'Submissão de projeto de TFG cadastrada com sucesso na plataforma!')
        return reverse(self.success_url)
    

class SubmissaoUpdateView(LoginRequiredMixin, AlunoRequiredMixin, UpdateView):
    model = Submissao
    form_class = SubmissaoForm
    template_name = 'appaluno/submissao_form.html'
    success_url = 'appaluno_submissao_list'
    
    def get_object(self, queryset=None):
        #Não deixa entrar no formulário de outro usuário
        pk = self.kwargs.get('pk')
        try:
            obj = Submissao.objects.get(pk=pk, aluno=self.request.user) 
        except:
            raise Http404("Você não tem acesso a esses dados")
        return obj         

    def form_valid(self, form):
        submissao = form.save(commit=False)
        submissao_teste = Submissao.objects.get(id=submissao.id)
        
        #verifica se a submissao esta finalizada
        try:
            if submissao.avaliacao and submissao.turma.disciplina.sigla == 'TFG1' and submissao.arquivo_documento_aceite and submissao.normativas == 'SIM' and submissao.arquivo_texto_preprojeto and submissao.termo_autoria == 'SIM' and submissao.arquivo_texto_tfgfinal and submissao.titulo:
                submissao.status = 'FINALIZADO'
            elif submissao.avaliacao and submissao.turma.disciplina.sigla == 'TFG2' and submissao.arquivo_documento_aceite and submissao.normativas == 'SIM' and submissao.termo_biblioteca and submissao.termo_autoria == 'SIM' and submissao.arquivo_texto_tfgfinal and submissao.titulo and submissao.resumo and submissao.palavras_chave:
                submissao.status = 'FINALIZADO'
        except:
            print("Submissão sem avaliação ainda. Atenção!!")

        # gera o termo de constituição de banca
        if submissao.termo_autoria == 'SIM' and submissao.arquivo_texto_tfgbanca:
            submissao.dt_aceite_termo_autoria = timezone.now()
            
        # gera o termo de autorização de publicação na biblioteca
        if submissao.termo_biblioteca == 'SIM' and submissao.arquivo_texto_tfgfinal:
            submissao.dt_aceite_termo_biblioteca = timezone.now()
            
        #verificar se os arquivos carregados são pdfs    
        if (not self.so_pdf(submissao)):
            messages.warning(self.request, 'Sistema suporta SOMENTE PDF!')
            return super(SubmissaoUpdateView, self).form_invalid(form)
        
        #verificar entregou versão final e preencheu título, resumo e palavras-chave
        try:
            if ( (submissao.avaliacao and submissao.turma.disciplina.sigla == 'TFG1' and submissao.arquivo_texto_tfgfinal and not submissao.titulo)
                or (submissao.avaliacao and submissao.turma.disciplina.sigla == 'TFG2' and submissao.arquivo_texto_tfgfinal and not submissao.titulo and not submissao.resumo and not submissao.palavras_chave) ):
                
                messages.warning(self.request, 'Atenção! Verifique se preencheu os campos como título por exemplo')
                return super(SubmissaoUpdateView, self).form_invalid(form)
        except:
            pass     
        
        submissao.save()
        # arquivo_texto_tfgorientador
        # arquivo_texto_tfgbanca
        # arquivo_texto_tfgrebanca
        # arquivo_texto_tfgfinal
        # print(self.object.avaliacao.avaliador_responsavel.email) 
        # print(self.object.avaliacao.avaliador_suplente.email) 
        # print(self.object.avaliacao.avaliador_convidado)        
        respostas = []
        if (submissao_teste.arquivo_texto_tfgorientador != submissao.arquivo_texto_tfgorientador):
            respostas.append("Arquivo de TFG para orientador")
        if (submissao_teste.arquivo_texto_tfgbanca != submissao.arquivo_texto_tfgbanca):
            respostas.append("Arquivo de TFG para banca")
        if (submissao_teste.arquivo_texto_tfgrebanca != submissao.arquivo_texto_tfgrebanca and submissao.arquivo_texto_tfgrebanca):
            respostas.append("Arquivo de TFG para REBANCA")
            try:
                """ enviar e-mail para avaliadores """
                if self.object.avaliacao.avaliador_convidado:
                    print("entrei na parte do convidado")
                    message = EmailMessage('usuario/email/submissao_rebanca_avaliador.html', {'submissao': self.object},
                        settings.EMAIL_HOST_USER, cc=[self.object.avaliacao.avaliador_responsavel.email, self.object.avaliacao.avaliador_suplente.email, self.object.avaliacao.avaliador_convidado.email])
                else:
                    message = EmailMessage('usuario/email/submissao_rebanca_avaliador.html', {'submissao': self.object},
                        settings.EMAIL_HOST_USER, cc=[self.object.avaliacao.avaliador_responsavel.email, self.object.avaliacao.avaliador_suplente.email])
                
                message.send()
            except:
                # alterar para outro tipo de requisição http
                messages.warning(self.request, "Mensagem, via email, sobre a REBANCA para os avaliadores não foi enviada por problemas com servidor!")
        if (submissao_teste.arquivo_texto_tfgfinal != submissao.arquivo_texto_tfgfinal):
            respostas.append("Arquivo de TFG Final")
        
        if respostas:    
            try:
                """ enviar e-mail para orientador """
                message = EmailMessage('usuario/email/submissao_atualizada_orientador.html', {'submissao': self.object, 'respostas': respostas},
                        settings.EMAIL_HOST_USER, to=[self.object.orientador.email])
                message.send()
            except:
                # alterar para outro tipo de requisição http
                messages.warning(self.request, "Submissão salva mas SEM NOTIFICAÇÃO PARA ORIENTADOR via email!!")
            
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Dados de projeto de TFG atualizados com sucesso na plataforma!')
        return reverse(self.success_url)

    def so_pdf(self, submissao):
        file_name, file_extension = os.path.splitext(str(submissao.arquivo_documento_aceite))
        if (submissao.arquivo_documento_aceite and file_extension != '.pdf'):
            return False

        file_name, file_extension = os.path.splitext(str(submissao.arquivo_texto_preprojeto))
        if (submissao.arquivo_texto_preprojeto and file_extension != '.pdf'):
            return False

        file_name, file_extension = os.path.splitext(str(submissao.arquivo_texto_tfgorientador))
        if (submissao.arquivo_texto_tfgorientador and file_extension != '.pdf'):
            return False
        
        file_name, file_extension = os.path.splitext(str(submissao.arquivo_texto_tfgbanca))
        if (submissao.arquivo_texto_tfgbanca and file_extension != '.pdf'):
            return False
        
        file_name, file_extension = os.path.splitext(str(submissao.arquivo_texto_tfgrebanca))
        if (submissao.arquivo_texto_tfgrebanca and file_extension != '.pdf'):
            return False

        file_name, file_extension = os.path.splitext(str(submissao.arquivo_texto_tfgfinal))
        if (submissao.arquivo_texto_tfgfinal and file_extension != '.pdf'):
            return False

        file_name, file_extension = os.path.splitext(str(submissao.arquivo_produto_tfgfinal))
        if (submissao.arquivo_produto_tfgfinal and file_extension != '.pdf'):
            return False

        return True


class AvaliacaoDetailView(LoginRequiredMixin, AlunoRequiredMixin, DetailView):
    model = Avaliacao
    template_name = 'appaluno/avaliacao_parecer_detail.html'


#modificado temporariamente
class SubmissaoSugestaoPreProjetoDetailView(LoginRequiredMixin, AlunoRequiredMixin, DetailView):
    model = Submissao
    template_name = 'appaluno/submissao_sugestao_preprojeto_detail.html'


class OrientacaoListView(LoginRequiredMixin, AlunoRequiredMixin, ListView):
    model = Orientacao
    template_name = 'appaluno/orientacao_list.html'
    
    def get_queryset(self):
        queryset = super(OrientacaoListView, self).get_queryset()
        return queryset.filter(submissao__aluno = self.request.user) 
    
    
class OrientacaoCreateView(LoginRequiredMixin, AlunoRequiredMixin, CreateView):
    model = Orientacao
    fields = ['data', 'hora', 'pauta', 'texto']
    template_name = 'appaluno/orientacao_form.html'
    success_url = 'appaluno_orientacao_list'
    
    def get_object(self, queryset=None):
        #Não deixa entrar no formulário de outro usuário
        pk = self.kwargs.get('pk')
        try:
            obj = Orientacao.objects.get(pk=pk, submissao__aluno=self.request.user) 
        except:
            raise Http404("Você não tem acesso a esses dados")
        return obj  

    def form_valid(self, form):
        try:
            orientacao = form.save(commit=False)
            orientacao.submissao = Submissao.objects.filter(aluno=self.request.user).order_by("id").last()
            orientacao.save()
        except Exception as e:
            messages.error(self.request, 'Erro ao gravar a ata da reunião. %s' % e)
        
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Reunião cadastrada com sucesso na plataforma!')
        return reverse(self.success_url)
        

class OrientacaoUpdateView(LoginRequiredMixin, AlunoRequiredMixin, UpdateView):
    model = Orientacao
    fields = ['pauta', 'texto']
    template_name = 'appaluno/orientacao_form.html'
    success_url = 'appaluno_orientacao_list'
    
    def get_object(self, queryset=None):
        #Não deixa entrar no formulário de outro usuário
        pk = self.kwargs.get('pk')
        try:
            obj = Orientacao.objects.get(pk=pk, submissao__aluno=self.request.user) 
        except:
            raise Http404("Você não tem acesso a esses dados")
        return obj         

    def form_valid(self, form):
        orientacao = form.save()    
        # try:
        #     """ enviar e-mail para orientador """
        #     message = EmailMessage('usuario/email/orientacao_atualizada_orientador.html', {'orientacao': self.object},
        #             settings.EMAIL_HOST_USER, to=[self.object.submissao.orientador.email])
        #     message.send()
        # except:
        #     # alterar para outro tipo de requisição http
        #     messages.warning(self.request, "Ata de reunião salva mas SEM NOTIFICAÇÃO PARA ORIENTADOR via email!!")
        
        return super().form_valid(form)
    
    def get_success_url(self):
        messages.success(self.request, 'Dados da reunião atualizados com sucesso na plataforma!')
        return reverse(self.success_url)


class OrientacaoDetailView(LoginRequiredMixin, AlunoRequiredMixin, DetailView):
    model = Orientacao
    template_name = 'appaluno/orientacao_detail.html'
