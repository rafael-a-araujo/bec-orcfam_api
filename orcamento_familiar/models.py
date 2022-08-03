from django.db import models


class Transacao(models.Model):
    TIPO = (
        ('D', 'Despesa'),
        ('R', 'Receita')
    )

    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=20, decimal_places=10)
    data = models.DateField()
    tipo = models.CharField(max_length=1, choices=TIPO, blank=False, null=False, default='D')

    def __str__(self):
        return f'{self.data} - {self.descricao} - {str(self.valor)} {self.tipo}'
