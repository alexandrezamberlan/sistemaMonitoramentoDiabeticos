from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from django.urls import reverse

from utils.gerador_hash import gerar_hash

class Alimento(models.Model):
    descricao = models.CharField('Descrição do alimento *', max_length=100, help_text='Seja sucinto na descrição do alimento. Lembre que é campo obrigatório')
    unidade = models.CharField('Unidade do alimento *', max_length=100, help_text='copo de 400 ml, ou colher, ou fatia, ou porção, por exemplo')
    calorias = models.DecimalField('Quantidade de calorias (g) da unidade desse alimento *', max_digits=5, decimal_places=0, help_text='Quantidade de calorias para a unidade definida desse alimento') 
    carboidratos = models.DecimalField('Quantidade de carboidratos (g) da unidade desse alimento *', max_digits=5, decimal_places=0, help_text='Quantidade de carboidratos para a unidade definida desse alimento') 
    fonte = models.CharField('Fonte ou referência desse alimento', null = True, blank = True, max_length=100, help_text='Use como referência alguma instituição, ou artigo, ou livro, por exemplo')
    slug = models.SlugField('Hash',max_length= 200, null=True, blank=True)

    objects = models.Manager()
    
    class Meta:
        ordering = ['descricao']
        verbose_name = 'alimento'
        verbose_name_plural = 'alimentos'

    def __str__(self):
        return f'{self.descricao} | {self.unidade}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gerar_hash()
        self.descricao = self.descricao.upper()
        self.unidade = self.unidade.upper()
        if self.fonte:
            self.fonte = self.fonte.upper()
        super(Alimento, self).save(*args, **kwargs)

    @property
    def get_absolute_url(self):
        return reverse('alimento_update', kwargs={'slug': self.slug})

    @property
    def get_delete_url(self):
        return reverse('alimento_delete', kwargs={'slug': self.slug})
