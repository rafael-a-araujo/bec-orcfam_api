import datetime
import decimal

from rest_framework.test import APITestCase
from orcamento_familiar.models import Receita
from django.urls import reverse
from rest_framework import status

class ReceitasTestCase(APITestCase):

    def setUp(self):
        self.list_url = reverse('Receitas-list')
        self.receita_1 = Receita.objects.create(
            descricao='Salário',
            valor=decimal.Decimal('1000.00'),
            data=datetime.date(day=10, month=9, year=2022)
        )
        self.receita_2 = Receita.objects.create(
            descricao='Juros', valor=decimal.Decimal('10.00'), data=datetime.date(day=10, month=9, year=2022)
        )

    def test_requisicao_get_para_listar_receitas(self):
        """Teste para verificar a requisição GET para listar as receitas"""
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_requisicao_post_para_criar_receita(self):
        """Teste para verificar a requisição POST para criar receita"""
        data = {
            'descricao': 'Salário Teste automatizado',
            'valor': decimal.Decimal('1000.00'),
            'data': '2022-10-10'
        }
        response = self.client.post(self.list_url, data=data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_requisicao_post_para_criar_receita_valor_negativo(self):
        """Teste para verificar a requisição POST para criar receita com valor negativo"""
        data = {
            'descricao': 'Salário valor negativo',
            'valor': decimal.Decimal('-1000.00'),
            'data': '2022-10-10'
        }
        response = self.client.post(self.list_url, data=data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_requisicao_post_para_criar_receita_duplicada(self):
        """
            Teste para verificar a requisição POST para criar receita duplicada.
            status response code HTTP 400 Bad Request
        """
        data = {
            'descricao': 'Salário',
            'valor': decimal.Decimal('1000.00'),
            'data': '2022-09-10'
        }
        response = self.client.post(self.list_url, data=data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_requisicao_delete_para_apagar_receita(self):
        """Teste para verificar requisição DELETE para deletar uma receita"""
        response = self.client.delete('/receitas/1/')
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_requisicao_put_para_atualizar_receita(self):
        """Teste para verificar requisição PUT para atualizar uma receita"""
        data = {
            'descricao': 'Salário atualizado',
            'valor': decimal.Decimal('1010.00'),
            'data': '2022-09-20'
        }
        response = self.client.put('/receitas/1/', data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_requisicao_put_para_atualizar_receita_com_descricao_e_mes_de_outra_ja_cadastrada(self):
        """Teste para verificar atualização de receita com descrição e mês de outra já cadastrada"""
        data = {
            'descricao': 'Juros',
            'valor': decimal.Decimal('1010.00'),
            'data': '2022-09-20'
        }
        response = self.client.put('/receitas/1/', data=data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_requisicao_get_para_detalhar_receita(self):
        """Teste para verificar requisição GET para detalhar uma receita"""
        response = self.client.get('/receitas/1/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)