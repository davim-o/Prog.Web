from django.urls import path
from loja.views.FavoritoView import favoritar_view, lista_favoritos_view

urlpatterns = [
    path('', lista_favoritos_view, name='lista_favoritos'),
    path('<int:produto_id>/', favoritar_view, name='favoritar'),
]
