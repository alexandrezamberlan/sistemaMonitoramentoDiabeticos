from __future__ import unicode_literals

from django.db.models import Max
from django.db.models import Subquery, OuterRef
from django.db import models
from django.urls import reverse

from utils.gerador_hash import gerar_hash


class DadosAtivoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
    
class ClientesDistintosManager(models.Manager):
    def get_queryset(self):
        subquery = (
            super()
            .get_queryset()
            .filter(is_active=True, cliente__id=OuterRef('cliente__id'))
            .order_by('-data_registro')
            .values('id')[:1]
        )

        return (
            super()
            .get_queryset()
            .filter(id__in=Subquery(subquery))
            .order_by('-data_registro')
        )

    
    # def get_queryset(self):
    #     return super().get_queryset().filter(is_active=True,cliente__tipo='CLIENTE')
    
    # def get_queryset(self):
    #     ultimos_ids = (
    #         super()
    #         .get_queryset()
    #         .filter(is_active=True)
    #         .values('cliente__nome')  # ou 'username'
    #         .annotate(ultimo_id=Max('cliente__id'))
    #         .values_list('ultimo_id', flat=True)
    #     )
    #     return super().get_queryset().filter(id__in=ultimos_ids)


class DiabeticosTipo1Manager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True,tipo_diabetes='DIABETES TIPO 1')


class DadoClinico(models.Model): 
    #1 campo da tupla fica no banco de dados
    #2 campo da tupla eh mostrado para o usuario
    TIPOS_DIABETES = (
        ('SEM DIABETES', 'Sem Diabetes'),
        ('PRE-DIABETES', 'Pré-Diabetes'),
        ('DIABETES GESTACIONAL', 'Diabetes Gestacional'),
        ('DIABETES TIPO 2', 'Diabetes Tipo 2'),
        ('DIABETES TIPO 1', 'Diabetes Tipo 1'),
    )    
    cliente = models.ForeignKey('usuario.Usuario', on_delete=models.PROTECT, related_name='dados_clinicos', verbose_name='Cliente *', help_text='* Campos obrigatórios')
    tipo_diabetes = models.CharField('Tipo de Diabetes', max_length=20, choices=TIPOS_DIABETES, null=True, blank=True)
    medicamentos = models.ManyToManyField('medicamento.Medicamento', null=True,blank=True, related_name='medicamentos', verbose_name='Medicamentos')
    bolus_alimentar = models.PositiveIntegerField('Bolus Alimentar (U)', null=True, blank=True, help_text='Unidades de insulina para cada 10g de carboidrato, por exemplo')
    bolus_correcao = models.PositiveIntegerField('Bolus Correção (U)', null=True, blank=True, help_text='Unidades de insulina para cada 10mg/dL acima da meta, por exemplo')
    glicemia_meta = models.PositiveIntegerField('Glicemia Meta (mg/dL)', null=True, blank=True)
    altura = models.PositiveIntegerField('Altura (cm)', null=True, blank=True)
    peso = models.PositiveIntegerField('Peso (kg)', null=True, blank=True)
    data_registro = models.DateField('Data do registro', auto_now=True)

    is_active = models.BooleanField('Ativo', default=False, help_text='Se ativo, o dado pode ser utilizado no sistema')
    slug = models.SlugField('Hash',max_length= 200, null=True, blank=True)

    objects = models.Manager()
    dados_ativos = DadosAtivoManager()
    clientes_distintos = ClientesDistintosManager()
    
    diabeticos_tipo1 = DiabeticosTipo1Manager()
    
    class Meta:
        ordering = ['cliente', '-data_registro']
        verbose_name = 'dado clínico'
        verbose_name_plural = 'dados clínicos'

    def __str__(self):
        return (
            f"{self.cliente} ({self.cliente.idade}) | "
            f"{self.tipo_diabetes or 'NI'} | "
            f"{self.bolus_alimentar or ''} | "
            f"{self.bolus_correcao or ''} | "
            f"{self.glicemia_meta or ''} | "
            f"{self.altura or ''} | "
            f"{self.peso or ''}"
        )


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
