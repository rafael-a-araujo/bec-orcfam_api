from django.contrib import admin
from orcamento_familiar.models import Transacao

class Transacoes(admin.ModelAdmin):
    list_display = ('id', 'data', 'descricao', 'valor', 'tipo')
    list_display_links = ('id', 'descricao')
    search_fields = ('descricao',)
    list_per_page = 20

admin.site.register(Transacao, Transacoes)