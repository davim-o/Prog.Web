from django.contrib.auth.models import User
from django.db import models
from .Produto import Produto


class Favorito(models.Model):
    user = models.ForeignKey(User, null=True, related_name='favoritos', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, null=True, related_name='favoritos', on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'produto')

    def __str__(self):
        return f'{self.user} - {self.produto}'
