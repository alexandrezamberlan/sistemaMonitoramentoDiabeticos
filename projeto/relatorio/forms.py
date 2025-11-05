from django import forms

from .models import Relatorio


class BuscaRelatorioForm(forms.Form):        
    pesquisa = forms.CharField(label='Pesquisa livre', required=False)
    
    