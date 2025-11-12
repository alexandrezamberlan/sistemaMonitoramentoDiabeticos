from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from .conecta_llm import Conecta
from utils.gerador_hash import gerar_hash

class RegistroRefeicao(models.Model):
    cliente = models.ForeignKey('dado_clinico.DadoClinico', verbose_name='Cliente ou paciente *', on_delete=models.PROTECT, help_text="* indica campo obrigatório.")
    alimentos = models.ManyToManyField('alimento.Alimento', verbose_name='Alimentos consumidos *', help_text="* indica campo obrigatório.", null=True, blank=True)
    registro_alimentacao = models.TextField('Registro alimentar *', help_text='Descreva o que foi consumido na refeição.', max_length=1000)
    glicemia_vigente = models.PositiveIntegerField('Glicemia vigente (mg/dL)', null=True, blank=True, help_text='Valor da glicemia antes da refeição, se disponível')
    quantidade_insulina_recomendada = models.PositiveIntegerField('Quantidade de insulina recomendada (U)', null=True, blank=True, help_text='Unidades de insulina recomendada para a refeição, se aplicável')
    nome_insulina = models.CharField('Nome da insulina recomendada', max_length=200, null=True, blank=True, help_text='Nome da insulina recomendada para a refeição, se aplicável')
    total_carboidratos = models.PositiveIntegerField('Total de carboidratos (g)', null=True, blank=True, help_text='Total de carboidratos consumidos na refeição, se conhecido')
    total_calorias = models.PositiveIntegerField('Total de calorias (kcal)', null=True, blank=True, help_text='Total de calorias consumidas na refeição, se conhecido')
    data_hora_registro = models.DateTimeField('Data e hora do registro', auto_now=True)
    quantidade_tokens_consumidos = models.PositiveIntegerField('Quantidade de tokens utilizados *', null=True, blank=True, default=0)
    slug = models.SlugField('Hash',max_length= 200, null=True, blank=True)

    objects = models.Manager()
    
    class Meta:
        ordering = ['cliente__cliente__nome', '-data_hora_registro']
        verbose_name = 'registro refeição'
        verbose_name_plural = 'registros refeições'

    def __str__(self):
        return f'{self.data_hora_registro}: {self.registro_alimentacao}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gerar_hash()
            
        medicamentos = [med.nome_comercial for med in self.cliente.medicamentos.all()] if self.cliente.medicamentos.exists() else []
        tipo_diabetes = self.cliente.tipo_diabetes or "SEM DIABETES"
        bolus_alimentar = self.cliente.bolus_alimentar or 1 #1 unidade de insulina para cada 10g de carboidrato
        bolus_correcao = self.cliente.bolus_correcao or 1 #1 unidade de insulina para cada 10mg/dL acima da meta
        glicemia_meta = self.cliente.glicemia_meta or 100
        glicemia_atual = self.glicemia_vigente
        descricao_alimentacao = self.registro_alimentacao
        
        contexto_json = Conecta.montar_json(medicamentos, tipo_diabetes, bolus_alimentar, bolus_correcao, glicemia_meta, glicemia_atual, descricao_alimentacao)
        total_tokens = 0
        resposta_json, total_tokens = Conecta.gerar_recomendacoes(contexto_json)
        
        # print("RESPOSTA JSON:", resposta_json)
        # print("TOTAL TOKENS:", total_tokens)
        
        lista_alimentos = []
        lista_alimentos, carboidratos, calorias, qtd_insulina, nome_insulina = Conecta.desmontar_json(resposta_json)
        self.total_carboidratos = int(carboidratos)
        self.total_calorias = int(calorias)
        self.quantidade_insulina_recomendada = int(qtd_insulina)
        self.nome_insulina = nome_insulina
        self.quantidade_tokens_consumidos = int(total_tokens)

        super(RegistroRefeicao, self).save(*args, **kwargs)

    @property
    def get_absolute_url(self):
        return reverse('registrorefeicao_update', kwargs={'slug': self.slug})

    @property
    def get_delete_url(self):
        return reverse('registrorefeicao_delete', kwargs={'slug': self.slug})
