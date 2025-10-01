from django import forms

from .models import Medicamento


class BuscaMedicamentoForm(forms.Form):        
    pesquisa = forms.CharField(label='Pesquisa livre', required=False)
    
    