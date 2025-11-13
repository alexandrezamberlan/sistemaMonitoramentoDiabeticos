from django import forms

from dado_clinico.models import DadoClinico
from medicamento.models import Medicamento
from usuario.models import Usuario
from registro_refeicao.models import RegistroRefeicao


class ClienteCreateForm(forms.ModelForm):
    nome = forms.CharField(label='Nome completo *', help_text='* Campos obrigatórios',required=True)
    
    instituicao = forms.CharField(label='Instituição a que pertence *', help_text='Registre a instituição, ou universidade, ou empresa',required=True)
    email = forms.EmailField(label='Email *', help_text='Use o email válido. Será usado para acessar sistema e recuperar senha!',required=True)
    celular = forms.CharField(label='Número celular com DDD *', help_text="Use DDD, por exemplo 55987619832",required=True)
    cpf = forms.CharField(label='CPF *',required=True)       
    
        
    class Meta:
        model = Usuario
        fields = ['nome','instituicao', 'email', 'celular', 'cpf']



class DadoClinicoClienteForm(forms.ModelForm):    
    medicamentos = forms.ModelMultipleChoiceField(label='Medicamentos', queryset=Medicamento.medicamentos_ativos.all(), required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = DadoClinico
        fields = ['tipo_diabetes', 'medicamentos', 'glicemia_meta', 'bolus_alimentar', 'bolus_correcao', 'altura', 'peso']

class ClienteRegistroRefeicaoForm(forms.ModelForm):

    cliente = forms.ModelChoiceField(label='Cliente', queryset=DadoClinico.clientes_distintos.all(), required=True)

    class Meta:
        model = RegistroRefeicao
        fields = ['registro_alimentacao', 'glicemia_vigente']