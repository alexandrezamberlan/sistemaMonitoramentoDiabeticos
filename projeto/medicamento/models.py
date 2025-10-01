from __future__ import unicode_literals

from django.db import models
from django.urls import reverse

from utils.gerador_hash import gerar_hash

class Medicamento(models.Model):
    #1 campo da tupla fica no banco de dados
    #2 campo da tupla eh mostrado para o usuario
    TIPOS_PRINCIPIOS_ATIVOS = (
        ('INSULINA ASPARTE', 'Insulina asparte'),
        ('INSULINA GLARGINA', 'Insulina glargina'),
        ('METFORMINA', 'Metformina'),
    )

    TIPOS_CLASSES_TERAPEUTICAS = (
        ('INSULINA RAPIDA', 'Insulina de ação rápida'),
        ('INSULINA BASAL', 'Insulina basal'),
        ('ORAL', 'Antidiabético oral'),
    )

    nome_comercial = models.CharField('Nome comercial *', max_length=25, help_text='ex: Novorapid, Lantus, Metformina')
    principio_ativo = models.CharField('Princípio ativo *', max_length=18, choices=TIPOS_PRINCIPIOS_ATIVOS)
    classe_terapeutica = models.CharField('Classe terapêutica *', max_length=25, choices=TIPOS_CLASSES_TERAPEUTICAS)
    slug = models.SlugField('Hash',max_length= 200, null=True, blank=True)

    objects = models.Manager()
    
    class Meta:
        ordering = ['nome_comercial']
        unique_together = ('nome_comercial', 'principio_ativo', 'classe_terapeutica')
        verbose_name = 'medicamento'
        verbose_name_plural = 'medicamentos'

    def __str__(self):
        return f'{self.nome_comercial} | {self.principio_ativo}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gerar_hash()
        self.nome_comercial = self.nome_comercial.upper()        
        super(Medicamento, self).save(*args, **kwargs)

    @property
    def get_absolute_url(self):
        return reverse('medicamento_update', kwargs={'slug': self.slug})

    @property
    def get_delete_url(self):
        return reverse('medicamento_delete', kwargs={'slug': self.slug})
