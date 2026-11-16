from django.urls import path
from loja.views.CategoriaView import categoria_listar, categoria_criar, categoria_editar, categoria_excluir

urlpatterns = [
    path('', categoria_listar, name='categorias'),
    path('criar/', categoria_criar, name='criar_categoria'),
    path('editar/<int:id>/', categoria_editar, name='editar_categoria'),
    path('excluir/<int:id>/', categoria_excluir, name='excluir_categoria'),
]
