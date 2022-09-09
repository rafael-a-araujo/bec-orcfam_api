from django.contrib import admin
from orcamento_familiar.models import Receita, Despesa


class Receitas(admin.ModelAdmin):
    list_display = ('id', 'data', 'descricao', 'valor')
    list_display_links = ('id', 'descricao')
    search_fields = ('descricao',)
    list_per_page = 20


class Despesas(admin.ModelAdmin):
    list_display = ('id', 'data', 'descricao', 'categoria', 'valor')
    list_display_links = ('id', 'descricao')
    search_fields = ('descricao',)
    list_per_page = 20


admin.site.register(Receita, Receitas)
admin.site.register(Despesa, Despesas)
