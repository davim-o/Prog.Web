from django.urls import path
from loja.views.ProdutoView import list_produto_view
from loja.views.ProdutoView import edit_produto_view
from loja.views.ProdutoView import edit_produto_postback
from loja.views.ProdutoView import details_produto_view
from loja.views.ProdutoView import delete_produto_view
from loja.views.ProdutoView import delete_produto_postback
from loja.views.ProdutoView import create_produto_view

urlpatterns = [
    path("", list_produto_view, name='produtos'),
    path("<int:id>", list_produto_view, name='produto'),
    path('edit/<int:id>', edit_produto_view,name='edit_produto' ),
    path("edit", edit_produto_postback, name= 'edit_produto_postback'),
    path("details/<int:id>", details_produto_view, name= 'details_produto'),
    path("delete/<int:id>", delete_produto_view, name='delete_produto'),
    path("delete", delete_produto_postback, name='delete_produto_postback'),
    path("create", create_produto_view, name= 'create_produto'),
]