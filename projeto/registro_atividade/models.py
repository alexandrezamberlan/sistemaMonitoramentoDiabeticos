from __future__ import unicode_literals

from django.db import models
from django.urls import reverse

from utils.gerador_hash import gerar_hash

class RegistroAtividade(models.Model):
    #1 campo da tupla fica no banco de dados
    #2 campo da tupla eh mostrado para o usuario
    BORG = (
        ('6 - MUITO FÁCIL', '6 - Muito fácil'),
        ('9 - FÁCIL', '9 - Fácil'),
        ('11 - RELATIVAMENTE FÁCIL', '11 - Relativamente fácil'),
        ('13 - LIGEIRAMENTE CANSATIVO', '13 - Ligeiramente cansativo'),
        ('15 - CANSATIVO', '15 - Cansativo'),
        ('17 - MUITO CANSATIVO', '17 - Muito cansativo'),
        ('19 - EXAUSTIVO', '19 - Exaustivo'),
    )
    cliente = models.ForeignKey('usuario.Usuario', verbose_name='Cliente ou paciente *', on_delete=models.PROTECT, help_text="* indica campo obrigatório.")
    data = models.DateField('Data da atividade física *', help_text='Use dd/mm/aaaa')
    hora = models.TimeField('Hora da atividade física *', help_text='Use hh:mm')    
    atividade = models.ForeignKey('exercicio.Exercicio', verbose_name="Atividade física realizada", on_delete=models.PROTECT)
    duracao = models.PositiveIntegerField('Quantos minutos em atividade *')
    esforco = models.CharField('Esforço subjetivo *', max_length=27, choices=BORG, help_text='Em relação ao esforço na atividade')   
    frequencia_cardiaca_media = models.PositiveIntegerField('Frequência cardíaca média durante a atividade', null=True, blank=True, help_text='Caso tenha utilizado um frequêncímetro durante a atividade') 
    total_calorias = models.PositiveIntegerField('Total de calorias queimadas durante a atividade', null=True, blank=True)
    slug = models.SlugField('Hash',max_length= 200, null=True, blank=True)

    objects = models.Manager()
    
    class Meta:
        ordering = ['data', 'hora', 'cliente__nome', 'atividade']
        verbose_name = 'registro atividade'
        verbose_name_plural = 'registros atividades'

    def __str__(self):
        return f'{self.data} | {self.hora}: {self.atividade} - {self.esforco}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gerar_hash()
        super(RegistroAtividade, self).save(*args, **kwargs)

    @property
    def get_absolute_url(self):
        return reverse('registroatividade_update', kwargs={'slug': self.slug})

    @property
    def get_delete_url(self):
        return reverse('registroatividade_delete', kwargs={'slug': self.slug})
