from __future__ import unicode_literals

from django.db import models
from django.urls import reverse

from utils.gerador_hash import gerar_hash

class RegistroRefeicao(models.Model):
    cliente = models.ForeignKey('dado_clinico.DadoClinico', verbose_name='Cliente ou paciente *', on_delete=models.PROTECT, help_text="* indica campo obrigatório.")
    alimentos = models.ManyToManyField('alimento.Alimento', verbose_name='Alimentos consumidos *', help_text="* indica campo obrigatório.", null=True, blank=True)
    registro_alimentacao = models.TextField('Registro alimentar *', help_text='Descreva o que foi consumido na refeição.', max_length=1000)
    glicemia_vigente = models.PositiveIntegerField('Glicemia vigente (mg/dL)', null=True, blank=True, help_text='Valor da glicemia antes da refeição, se disponível')
    quantidade_insulina_recomendada = models.PositiveIntegerField('Quantidade de insulina recomendada (U)', null=True, blank=True, help_text='Unidades de insulina recomendada para a refeição, se aplicável')
    total_carboidratos = models.PositiveIntegerField('Total de carboidratos (g)', null=True, blank=True, help_text='Total de carboidratos consumidos na refeição, se conhecido')
    total_calorias = models.PositiveIntegerField('Total de calorias (kcal)', null=True, blank=True, help_text='Total de calorias consumidas na refeição, se conhecido')
    data_hora_registro = models.DateTimeField('Data e hora do registro', auto_now=True)
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
        super(RegistroRefeicao, self).save(*args, **kwargs)

    @property
    def get_absolute_url(self):
        return reverse('registrorefeicao_update', kwargs={'slug': self.slug})

    @property
    def get_delete_url(self):
        return reverse('registrorefeicao_delete', kwargs={'slug': self.slug})
