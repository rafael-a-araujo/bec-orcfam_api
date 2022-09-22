from django.db import models
from orcamento_familiar.enums import Categorias

class Transacao(models.Model):
    class Meta:
        abstract = True

    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=20, decimal_places=10)
    data = models.DateField()

    def __str__(self):
        return f'{self.data} - {self.descricao} - {str(self.valor)} '

class Despesa(Transacao):

    class Meta:
        verbose_name_plural = 'Despesas'
        verbose_name = 'Despesa'

    categoria = models.CharField(max_length=3, choices=Categorias.choices, blank=True, default=Categorias.OUTRAS)

class Receita(Transacao):

    class Meta:
        verbose_name_plural = 'Receitas'
        verbose_name = 'Receita'

