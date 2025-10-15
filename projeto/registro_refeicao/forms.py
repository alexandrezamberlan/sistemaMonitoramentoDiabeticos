from django import forms

from .models import RegistroRefeicao
from dado_clinico.models import DadoClinico

class BuscaRegistroRefeicaoForm(forms.Form):        
    pesquisa = forms.CharField(label='Pesquisa livre', required=False)
    
    
class RegistroRefeicaoForm(forms.ModelForm):

    cliente = forms.ModelChoiceField(label='Cliente', queryset=DadoClinico.clientes_distintos.all(), required=True)

    class Meta:
        model = RegistroRefeicao
        fields = ['cliente', 'registro_alimentacao', 'glicemia_vigente']