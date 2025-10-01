from django import forms

from .models import Exercicio


class BuscaExercicioForm(forms.Form):        
    pesquisa = forms.CharField(label='Pesquisa livre', required=False)
    
    