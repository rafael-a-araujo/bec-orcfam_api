import decimal

from django.db.models import Sum
from rest_framework import viewsets, generics
from rest_framework.response import Response

from orcamento_familiar.models import Receita, Despesa
from orcamento_familiar.serializers import ReceitaSerializer, DespesaSerializer, ListaReceitasAnoMesSerializer, \
    ListaDespesasAnoMesSerializer


class ReceitasViewSet(viewsets.ModelViewSet):
    queryset = Receita.objects.all()
    serializer_class = ReceitaSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned incomes based on description,
        by filtering against a 'descricao' query parameter in the URL.
        """
        queryset = Receita.objects.all()
        descricao = self.request.query_params.get('descricao')
        if descricao is not None:
            queryset = queryset.filter(descricao__contains=descricao)
        return queryset


class ListaReceitasAnoMes(generics.ListAPIView):
    """Listando as receitas de mês/ano específico"""
    def get_queryset(self):
        queryset = Receita.objects.filter(data__year=self.kwargs['ano'], data__month=self.kwargs['mes'])
        return queryset
    serializer_class = ListaReceitasAnoMesSerializer


class DespesasViewSet(viewsets.ModelViewSet):
    queryset = Despesa.objects.all()
    serializer_class = DespesaSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned incomes based on description,
        by filtering against a 'descricao' query parameter in the URL.
        """
        queryset = Despesa.objects.all()
        descricao = self.request.query_params.get('descricao')
        if descricao is not None:
            queryset = queryset.filter(descricao__contains=descricao)
        return queryset

class ListaDespesasAnoMes(generics.ListAPIView):
    """Listando as despesas de mês/ano específico"""
    def get_queryset(self):
        queryset = Despesa.objects.filter(data__year=self.kwargs['ano'], data__month=self.kwargs['mes'])
        return queryset
    serializer_class = ListaDespesasAnoMesSerializer



class ExibeResumoAnoMes(generics.ListAPIView):

    def get(self, request, *args, **kwargs):

        total_receitas = self.extrai_total(Receita, self.kwargs['ano'], self.kwargs['mes'])
        total_despesas = self.extrai_total(Despesa, self.kwargs['ano'], self.kwargs['mes'])

        saldo_mes = total_receitas - total_despesas

        total_despesas_por_categoria = Despesa.objects.values('categoria').annotate(total=Sum('valor')).\
            filter(data__year=self.kwargs['ano'], data__month=self.kwargs['mes'])

        return Response({
            'total_receitas': total_receitas,
            'total_despesas': total_despesas,
            'saldo_mes': saldo_mes,
            'total_despesas_por_categoria' : total_despesas_por_categoria,
        })

    def extrai_total(self, transacao, ano, mes):
        total = transacao.objects.filter(data__year=ano, data__month=mes).aggregate(Sum('valor'))['valor__sum']
        if total is None:
            total = decimal.Decimal(0.0)
        return total
