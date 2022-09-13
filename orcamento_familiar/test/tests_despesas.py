import datetime
import decimal

from rest_framework.test import APITestCase
from orcamento_familiar.models import Despesa
from orcamento_familiar.enums import Categorias
from django.urls import reverse
from rest_framework import status

class DespesasTestCase(APITestCase):

    def setUp(self):
        self.list_url = reverse('Despesas-list')
        self.despesa_1 = Despesa.objects.create(
            descricao='Aluguel',
            valor=decimal.Decimal('500.00'),
            data=datetime.date(day=10, month=9, year=2022),
            categoria=Categorias.MORADIA
        )
        self.despesa_2 = Despesa.objects.create(
            descricao='Energia Elétrica',
            valor=decimal.Decimal('100.00'),
            data=datetime.date(day=10, month=9, year=2022),
            categoria=Categorias.MORADIA
        )

    def test_requisicao_get_para_listar_despesas(self):
        """Teste para verificar a requisição GET para listar as despesas"""
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_requisicao_post_para_criar_despesa(self):
        """Teste para verificar a requisição POST para criar despesa"""
        data = {
            'descricao': 'Restaurante',
            'valor': decimal.Decimal('1000.00'),
            'data': '2022-10-10',
            'categoria': Categorias.ALIMENTACAO
        }
        response = self.client.post(self.list_url, data=data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_requisicao_post_para_criar_despesa_valor_negativo(self):
        """Teste para verificar a requisição POST para criar despesa com valor negativo"""
        data = {
            'descricao': 'Despesa com valor negativo',
            'valor': decimal.Decimal('-1000.00'),
            'data': '2022-10-10'
        }
        response = self.client.post(self.list_url, data=data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_requisicao_post_para_criar_despesa_duplicada(self):
        """
            Teste para verificar a requisição POST para criar despesa duplicada.
            status response code HTTP 400 Bad Request
        """
        data = {
            'descricao': 'Aluguel',
            'valor': decimal.Decimal('1000.00'),
            'data': '2022-09-10'
        }
        response = self.client.post(self.list_url, data=data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_requisicao_delete_para_apagar_despesa(self):
        """Teste para verificar requisição DELETE para deletar uma despesa"""
        response = self.client.delete('/despesas/1/')
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_requisicao_put_para_atualizar_despesa(self):
        """Teste para verificar requisição PUT para atualizar uma despesa"""
        data = {
            'descricao': 'Aluguel Atualizado',
            'valor': decimal.Decimal('1010.00'),
            'data': '2022-09-20'
        }
        response = self.client.put('/despesas/1/', data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_requisicao_put_para_atualizar_despesa_com_descricao_e_mes_de_outra_ja_cadastrada(self):
        """Teste para verificar atualização de despesa com descrição e mês de outra já cadastrada"""
        data = {
            'descricao': 'Energia Elétrica',
            'valor': decimal.Decimal('1010.00'),
            'data': '2022-09-20'
        }
        response = self.client.put('/despesas/1/', data=data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_requisicao_get_para_detalhar_despesa(self):
        """Teste para verificar requisição GET para detalhar uma despesa"""
        response = self.client.get('/despesas/1/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)