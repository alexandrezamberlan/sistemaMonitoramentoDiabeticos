from django import forms

from .models import DadoClinico


class BuscaDadoClinicoForm(forms.Form):        
    pesquisa = forms.CharField(label='Pesquisa livre', required=False)
    
    