from django import forms

from .models import RegistroAtividade


class BuscaRegistroAtividadeForm(forms.Form):        
    pesquisa = forms.CharField(label='Pesquisa livre', required=False)
    
    