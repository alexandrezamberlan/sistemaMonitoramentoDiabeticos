from django import forms
from alimento.models import Alimento


class BuscaRefeicaoForm(forms.Form):
    alimento = forms.CharField(label='Alimento de pesquisa', required=False)
    data = forms.CharField(label='Data de pesquisa', required=False, help_text='Pesquise por dia ou mês ou ano ou data dd/mm/aaaa')