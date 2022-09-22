import decimal

from django.db.models import Sum
from rest_framework import viewsets, generics, views, permissions, status
from rest_framework.response import Response

from orcamento_familiar.models import Receita, Despesa
from orcamento_familiar.serializers import ReceitaSerializer, DespesaSerializer, ListaReceitasAnoMesSerializer, \
    ListaDespesasAnoMesSerializer, LoginSerializer


class TransacoesViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        """
        Optionally restricts the returned transactions based on description,
        by filtering against a 'descricao' query parameter in the URL.
        """
        queryset = self.model.objects.all()
        descricao = self.request.query_params.get('descricao')
        if descricao is not None:
            queryset = queryset.filter(descricao__contains=descricao)
        return queryset

class ReceitasViewSet(TransacoesViewSet):
    model = Receita
    queryset = Receita.objects.all()
    serializer_class = ReceitaSerializer

class DespesasViewSet(TransacoesViewSet):
    model = Despesa
    queryset = Despesa.objects.all()
    serializer_class = DespesaSerializer

class ListaTransacoesAnoMes(generics.ListAPIView):
    """Lista as transações de mês/ano específico"""
    def get_queryset(self):
        queryset = self.model_class.objects.filter(data__year=self.kwargs['ano'], data__month=self.kwargs['mes'])
        return queryset

class ListaReceitasAnoMes(ListaTransacoesAnoMes):
    model_class = Receita
    serializer_class = ListaReceitasAnoMesSerializer

class ListaDespesasAnoMes(ListaTransacoesAnoMes):
    model_class = Despesa
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


class LoginView(views.APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)