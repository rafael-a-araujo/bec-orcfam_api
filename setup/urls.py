"""setup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from orcamento_familiar.views import ReceitasViewSet, DespesasViewSet, ListaReceitasAnoMes, ListaDespesasAnoMes,\
    ExibeResumoAnoMes, LoginView

router = routers.DefaultRouter()
router.register('receitas', ReceitasViewSet, basename='Receitas')
router.register('despesas', DespesasViewSet, basename='Despesas')
#router.register('resumo', ExibeResumoAnoMes.as_view(), basename='Resumo')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view()),
    path('', include(router.urls)),
    path('receitas/<int:ano>/<int:mes>/', ListaReceitasAnoMes.as_view()),
    path('despesas/<int:ano>/<int:mes>/', ListaDespesasAnoMes.as_view()),
    path('resumo/<int:ano>/<int:mes>/', ExibeResumoAnoMes.as_view()),
]
