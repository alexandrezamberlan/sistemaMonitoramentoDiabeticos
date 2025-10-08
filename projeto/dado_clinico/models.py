from __future__ import unicode_literals

from django.db import models
from django.urls import reverse

from utils.gerador_hash import gerar_hash


class DadosAtivoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class DadoClinico(models.Model):    
    cliente = models.ForeignKey('usuario.Usuario', on_delete=models.PROTECT, related_name='dados_clinicos', verbose_name='Cliente *', help_text='* Campos obrigatórios')
    medicamentos = models.ManyToManyField('medicamento.Medicamento', null=True,blank=True, related_name='medicamentos', verbose_name='Medicamentos')
    bolus_alimentar = models.PositiveIntegerField('Bolus Alimentar (U)', null=True, blank=True, help_text='Unidades de insulina para cada 10g de carboidrato, por exemplo')
    bolus_correcao = models.PositiveIntegerField('Bolus Correção (U)', null=True, blank=True, help_text='Unidades de insulina para cada 10mg/dL acima da meta, por exemplo')
    altura = models.PositiveIntegerField('Altura (cm)', null=True, blank=True)
    peso = models.PositiveIntegerField('Peso (kg)', null=True, blank=True)
    data_registro = models.DateField('Data do registro', auto_now=True)

    is_active = models.BooleanField('Ativo', default=False, help_text='Se ativo, o dado pode ser utilizado no sistema')
    slug = models.SlugField('Hash',max_length= 200, null=True, blank=True)

    objects = models.Manager()
    dados_ativos = DadosAtivoManager()
    
    class Meta:
        ordering = ['cliente']
        verbose_name = 'dado clínico'
        verbose_name_plural = 'dados clínicos'

    def __str__(self):
        return f'{self.cliente} | {self.bolus_alimentar} | {self.bolus_correcao} | {self.altura} | {self.peso}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gerar_hash()

        super(DadoClinico, self).save(*args, **kwargs)

    @property
    def get_absolute_url(self):
        return reverse('dadoclinico_update', kwargs={'slug': self.slug})

    @property
    def get_delete_url(self):
        return reverse('dadoclinico_delete', kwargs={'slug': self.slug})
