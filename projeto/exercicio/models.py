from __future__ import unicode_literals

from django.db import models
from django.urls import reverse

from utils.gerador_hash import gerar_hash

class Exercicio(models.Model):
    #1 campo da tupla fica no banco de dados
    #2 campo da tupla eh mostrado para o usuario
    TIPOS = (
        ('AERÓBICA', 'Aeróbica'),
        ('ANAERÓBICA', 'Anaeróbica'),
        ('ALONGAMENTO', 'Alongamento'),
    )

    nome = models.CharField('Nome da atividade *', unique=True, max_length=25, help_text='* Campos obrigatórios')
    descricao = models.TextField('Detalhes da atividade física', null=True, blank=True, max_length=1000, help_text='Se necessário, explique a atividade física')
    tipo = models.CharField('Tipo de atividade *', max_length=15, choices=TIPOS, help_text='Em relação ao consumo de oxigênio')
    slug = models.SlugField('Hash',max_length= 200, null=True, blank=True)

    objects = models.Manager()
    
    class Meta:
        ordering = ['nome']
        verbose_name = 'exercicio'
        verbose_name_plural = 'exercicios'

    def __str__(self):
        return f'{self.nome} | {self.tipo}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gerar_hash()
        self.nome = self.nome.upper()        
        if self.descricao:
            self.descricao = self.descricao.upper()
        super(Exercicio, self).save(*args, **kwargs)

    @property
    def get_absolute_url(self):
        return reverse('exercicio_update', kwargs={'slug': self.slug})

    @property
    def get_delete_url(self):
        return reverse('exercicio_delete', kwargs={'slug': self.slug})
