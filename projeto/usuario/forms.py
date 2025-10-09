from django import forms
from django.db import models

from .models import Usuario

class BuscaUsuarioForm(forms.Form):    
    pesquisa = forms.CharField(label='Pesquisa livre', required=False)
       
    
class UsuarioRegisterForm(forms.ModelForm):
    TIPOS_USUARIOS = (
        ('CLIENTE', 'Cliente'),
    )
    
    TIPO_SEXO = (
        ('FEMININO', 'Feminino'),
        ('MASCULINO', 'Masculino'),
    )

    tipo = forms.ChoiceField(label='Tipo *',choices=TIPOS_USUARIOS, help_text='Este processo cadastra somente cliente', required=True)
    nome = forms.CharField(label='Nome completo *', help_text='* Campos obrigatórios',required=True)
    data_nascimento = forms.DateField(label='Data de nascimento', help_text='Informe sua data de nascimento (dd/mm/aaaa)', required=True, widget=forms.DateInput(format=('%d/%m/%Y'), attrs={'placeholder':'dd/mm/aaaa'}))
    sexo = forms.ChoiceField(label='Sexo *', choices=TIPO_SEXO, help_text='Campo obrigatório para cálculo de gasto energético/calórico e consumo alimentar', required=True)
    email = forms.EmailField(label='Email *', help_text='Use o email válido. Será usado para acessar sistema e recuperar senha!',required=True)
    celular = forms.CharField(label='Número celular com DDD *', help_text="Use DDD, por exemplo 55987619832",required=True)
    cpf = forms.CharField(label='CPF *',required=True)    
    password = forms.CharField(label= "Senha *", widget=forms.PasswordInput,required=True)
    aceita_termo = forms.BooleanField(label='Aceito', required=True, help_text='Se marcado, você aceita o termo de consentimento de uso do sistema')
        
    class Meta:
        model = Usuario
        fields = ['tipo','nome','data_nascimento','sexo', 'email', 'celular', 'cpf', 'password','aceita_termo']
