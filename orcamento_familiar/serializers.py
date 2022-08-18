from rest_framework import serializers
from orcamento_familiar.models import Transacao


class ReceitaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transacao
        fields = ['descricao', 'valor', 'data']
        verbose_name_plural = "Transações"

    def validate(self, data):
        """
        Verifica se existe receita com a mesma descrição para este mês.
        """
        receitas_ja_cadastradas = Transacao.objects.filter(descricao=data['descricao'], data__month=data['data'].month, data__year=data['data'].year, tipo='R')
        if receitas_ja_cadastradas:
            if self.is_create_receita():
                raise serializers.ValidationError("Cadastro de receita duplicada - esta receita já existe neste mês.")
            elif self.is_update_receita():
                id = receitas_ja_cadastradas[0].id
                if self.is_outra_receita(id):
                    raise serializers.ValidationError("Atualização de receita - a descrição está sendo atualizada para outra que já existe neste mês.")
        return data

    def create(self, validated_data):
        validated_data['tipo'] = 'R'
        return super(ReceitaSerializer, self).create(validated_data)

    def is_create_receita(self):
        return self.instance is None

    def is_update_receita(self):
        return self.instance is not None

    def is_outra_receita(self, id):
        return not self.instance.id == id


class DespesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transacao
        fields = ['descricao', 'valor', 'data']
        verbose_name_plural = "Transações"

    def validate(self, data):
        """
        Verifica se existe despesa com a mesma descrição para este mês.
        """
        despesas_ja_cadastradas = Transacao.objects.filter(descricao=data['descricao'], data__month=data['data'].month, data__year=data['data'].year, tipo='D')
        if despesas_ja_cadastradas:
            if self.is_create_despesa():
                raise serializers.ValidationError("Cadastro de despesa duplicada - esta despesa já existe neste mês.")
            elif self.is_update_despesa():
                id = despesas_ja_cadastradas[0].id
                if self.is_outra_despesa(id):
                    raise serializers.ValidationError(
                        "Atualização de despesa - a descrição está sendo atualizada para outra que já existe neste mês.")
        return data

    def create(self, validated_data):
        validated_data['tipo'] = 'D'
        return super(DespesaSerializer, self).create(validated_data)

    def is_create_despesa(self):
        return self.instance is None

    def is_update_despesa(self):
        return self.instance is not None

    def is_outra_despesa(self, id):
        return not self.instance.id == id