from django.contrib import admin
from .models import Categoria, Fabricante, Produto, Usuario

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('Categoria', 'criado_em', 'alterado_em')
    search_fields = ('Categoria',)
    ordering = ('Categoria',)

@admin.register(Fabricante)
class FabricanteAdmin(admin.ModelAdmin):
    list_display = ('fabricante', 'criado_em', 'alterado_em')
    search_fields = ('fabricante',)
    ordering = ('fabricante',)

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    date_hierarchy = 'criado_em'
    list_display = ('produtoo', 'preco', 'categoria', 'fabricante', 'destaque', 'promocao')
    list_filter = ('destaque', 'promocao', 'categoria', 'fabricante')
    search_fields = ('produtoo', 'categoria__Categoria', 'fabricante__fabricante')
    empty_value_display = 'Vazio'

admin.site.register(Usuario)
