from django import forms

from medicamento.models import Medicamento
from usuario.models import Usuario

from .models import DadoClinico


class BuscaDadoClinicoForm(forms.Form):        
    pesquisa = forms.CharField(label='Pesquisa livre', required=False)
    
    
class DadoClinicoForm(forms.ModelForm):
    
    cliente = forms.ModelChoiceField(label='Cliente', queryset=Usuario.clientes.all(), required=True)
    medicamentos = forms.ModelMultipleChoiceField(label='Medicamentos', queryset=Medicamento.medicamentos_ativos.all(), required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = DadoClinico
        fields = ['cliente', 'medicamentos', 'bolus_alimentar', 'bolus_correcao', 'altura', 'peso', 'is_active']