from django.utils.translation import gettext_lazy as _
from django.db import models


class Categorias(models.TextChoices):

    ALIMENTACAO = 'ALI', _('Alimentação')
    SAUDE = 'SAU', _('Saúde')
    MORADIA = 'MOR', _('Moradia')
    TRANSPORTE = 'TRA', _('Transporte')
    EDUCACAO = 'EDU', _('Educação')
    LAZER = 'LAZ', _('Lazer')
    IMPREVISTOS = 'IMP', _('Imprevistos')
    OUTRAS = 'OUT', _('Outras')