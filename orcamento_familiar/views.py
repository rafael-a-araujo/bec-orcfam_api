import datetime
import decimal

from django.http import JsonResponse


def transacoes(request):
    if request.method == 'GET':
        transacao = {'id':1, 'descricao':'salario'}
        return JsonResponse(transacao)
