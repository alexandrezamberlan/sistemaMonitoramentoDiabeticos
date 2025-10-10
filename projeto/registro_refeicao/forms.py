from django import forms

from .models import RegistroRefeicao


class BuscaRegistroRefeicaoForm(forms.Form):        
    pesquisa = forms.CharField(label='Pesquisa livre', required=False)
    
    