from django.db import models
from .Categoria import Categoria
from .Fabricante import Fabricante


class Produto(models.Model):
    produtoo = models.CharField(max_length=100)
    destaque = models.BooleanField(default=True)
    promocao = models.BooleanField(default=True)
    msgPromocao = models.CharField(max_length=100, null=True, blank=True)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    categoria = models.ForeignKey(
        Categoria,
        null=True,
        related_name='categoria' ,
        on_delete=models.SET_NULL,
    )
    fabricante = models.ForeignKey(
        Fabricante,
        null=True,
        related_name='fabricantee' ,
        on_delete=models.SET_NULL,
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    alterado_em = models.DateTimeField(auto_now=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.produtoo
