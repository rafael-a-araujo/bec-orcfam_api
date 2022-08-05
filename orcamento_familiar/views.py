from rest_framework import viewsets
from orcamento_familiar.models import Transacao
from orcamento_familiar.serializers import ReceitaSerializer


class ReceitasViewSet(viewsets.ModelViewSet):
    queryset = Transacao.objects.filter(tipo='R')
    serializer_class = ReceitaSerializer

