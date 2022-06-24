from django.contrib.auth.models import User
from django.db import models

from Usuarios.models import Usuarios

# Create your models here.


class Solicitudes(models.Model):
    Envio = models.BooleanField()
    FROM_usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    Recibio = models.BooleanField()
    TO_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Solicitud"
        verbose_name_plural = "Solicitudes"


class Amigos(models.Model):

    Amigo1 = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    # Amigo2=models.ForeignKey(Usuairos, on_delete=models.CASCADE)
    Amigo2 = models.IntegerField(null=False)  # Este es el Usuario id del amigo

    class Meta:
        verbose_name = "Amigo"
        verbose_name_plural = "Amigos"


class Bloqueos(models.Model):

    Bloqueador = models.ForeignKey(User, on_delete=models.CASCADE)
    Bloqueado = models.IntegerField(null=False)  # Este es el Usuario id del bloqueado

    class Meta:
        verbose_name = "Bloqueo"
        verbose_name_plural = "Bloqueos"
