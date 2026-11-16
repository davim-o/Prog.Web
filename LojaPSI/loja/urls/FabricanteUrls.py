from django.urls import path
from loja.views.FabricanteView import fabricante_listar, fabricante_criar, fabricante_editar, fabricante_excluir

urlpatterns = [
    path('', fabricante_listar, name='fabricantes'),
    path('criar/', fabricante_criar, name='criar_fabricante'),
    path('editar/<int:id>/', fabricante_editar, name='editar_fabricante'),
    path('excluir/<int:id>/', fabricante_excluir, name='excluir_fabricante'),
]
