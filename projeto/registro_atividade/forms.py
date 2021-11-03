from django import forms
from registro_atividade.models import RegistroAtividade


class BuscaAtividadeForm(forms.Form):
    atividade = forms.CharField(label='Atividade a ser pesquisada', required=False)
    data = forms.CharField(label='Data de pesquisa', required=False, help_text='Pesquise por dia ou mês ou ano ou data dd/mm/aaaa')