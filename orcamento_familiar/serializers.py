from rest_framework import serializers
from orcamento_familiar.models import Transacao


class ReceitaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transacao
        fields = ['id', 'descricao', 'valor', 'data']
        verbose_name_plural = "Transações"

    def validate(self, data):
        """
        Verifica se existe receita com a mesma descrição para este mês.
        """
        queryset = Transacao.objects.filter(descricao=data['descricao'], data__month=data['data'].month)
        if queryset:
            raise serializers.ValidationError("Receita duplicada - esta receita já existe neste mês.")
        return data

    def create(self, validated_data):
        validated_data['tipo'] = 'R'
        return super(ReceitaSerializer, self).create(validated_data)