from django import forms
from django.db import models

from usuario.models import Usuario
from .models import Alimento


class BuscaAlimentoForm(forms.Form):        
    pesquisa = forms.CharField(label='Pesquisa livre', required=False)
    
    