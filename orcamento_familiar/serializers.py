from django.contrib.auth import authenticate

from rest_framework import serializers

from orcamento_familiar.enums import Categorias
from orcamento_familiar.models import Transacao, Receita, Despesa

class TransacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transacao
        fields = ['descricao', 'valor', 'data']
        abstract = True

    def is_create(self):
        return self.instance is None

    def is_update(self):
        return self.instance is not None

    def is_outra(self, id):
        return not self.instance.id == id

    def validate(self, data):
        """
        Validação de transação
        - Valor precisa ser positivo.
        """
        if data['valor'] <= 0.0:
            raise serializers.ValidationError("É necessário que o valor seja positivo - maior que 0.0.")

        transacoes_ja_cadastradas = self.Meta.model.objects.filter(descricao=data['descricao'], data__month=data['data'].month,
                                                         data__year=data['data'].year)
        if transacoes_ja_cadastradas:
            if self.is_create():
                raise serializers.ValidationError(f'Cadastro de {self.Meta.verbose_name} duplicada - esta {self.Meta.verbose_name} já existe neste mês.')
            elif self.is_update():
                id = transacoes_ja_cadastradas[0].id
                if self.is_outra(id):
                    raise serializers.ValidationError(
                        f'Atualização de {self.Meta.verbose_name} - a descrição está sendo atualizada para outra que já existe neste mês.')
        return data


class ReceitaSerializer(TransacaoSerializer):

    class Meta(TransacaoSerializer.Meta):
        model = Receita
        verbose_name_plural = "Receitas"
        verbose_name = "Receita"


class DespesaSerializer(TransacaoSerializer):
    class Meta(TransacaoSerializer.Meta):
        model = Despesa
        fields = ['descricao', 'valor', 'data', 'categoria']
        verbose_name_plural = "Despesas"
        verbose_name = "Despesas"

    def create(self, validated_data):
        if not validated_data['categoria']:
            validated_data['categoria'] = Categorias.OUTRAS
        return super(DespesaSerializer, self).create(validated_data)


class ListaReceitasAnoMesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receita
        fields = ['descricao', 'valor', 'data']

class ListaDespesasAnoMesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Despesa
        fields = ['descricao', 'valor', 'data', 'categoria']


class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take username and password from request
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs