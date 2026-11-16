from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    perfil = models.IntegerField(choices=((1, 'Admin'), (2, 'Usuario')), default=2)
    aniversario = models.DateField(default=None, null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    alterado_em = models.DateTimeField(auto_now=True)
    token = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_usuario(sender, instance, created, **kwargs):
        if created:
            Usuario.objects.get_or_create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_usuario(sender, instance, **kwargs):
        try:
            instance.usuario.save()
        except Usuario.DoesNotExist:
            Usuario.objects.create(user=instance)
