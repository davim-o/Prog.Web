from django.contrib.auth.models import User
from django.db import models
from .Produto import Produto


class Carrinho(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, related_name='carrinhos', on_delete=models.SET_NULL)
    situacao = models.PositiveIntegerField(default=0)
    confirmado_em = models.DateTimeField(null=True, blank=True)

    @property
    def total(self):
        return sum((item.total for item in self.itens.all()), 0)

    def __str__(self):
        return str(self.criado_em)


class CarrinhoItem(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True)
    carrinho = models.ForeignKey(Carrinho, null=True, related_name='itens', on_delete=models.SET_NULL)
    produto = models.ForeignKey(Produto, null=True, related_name='carrinhos', on_delete=models.SET_NULL)
    quantidade = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=8, decimal_places=2)

    @property
    def total(self):
        if self.produto is None:
            return 0
        return self.quantidade * self.preco

    def __str__(self):
        return str(self.produto)
