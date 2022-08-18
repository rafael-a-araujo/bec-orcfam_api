from rest_framework import viewsets
from orcamento_familiar.models import Transacao
from orcamento_familiar.serializers import ReceitaSerializer, DespesaSerializer


class ReceitasViewSet(viewsets.ModelViewSet):
    queryset = Transacao.objects.filter(tipo='R')
    serializer_class = ReceitaSerializer


class DespesasViewSet(viewsets.ModelViewSet):
    queryset = Transacao.objects.filter(tipo='D')
    serializer_class = DespesaSerializer