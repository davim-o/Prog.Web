from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

PERFIL = (
    (1, 'Admin'),
    (2, 'Usuario'),
)

from .Fabricante import Fabricante
from .Categoria import Categoria
from .Produto import Produto
from .Usuario import Usuario
from .Carrinho import Carrinho, CarrinhoItem
from .Favorito import Favorito

__all__ = [
    'User', 'models', 'post_save', 'receiver', 'PERFIL',
    'Fabricante', 'Categoria', 'Produto', 'Usuario',
    'Carrinho', 'CarrinhoItem', 'Favorito',
]
