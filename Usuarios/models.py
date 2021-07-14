from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Usuarios(models.Model):
    usuario=models.OneToOneField(User, on_delete=models.CASCADE)
    Descripcion=models.CharField(max_length=50, null=True)
    Foto=models.ImageField(upload_to='Usuarios', null=True, blank=True)
    Email=models.EmailField(max_length=50, null=False)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name='Usuario'
        verbose_name_plural='Usuarios'
    def __str__ (self):
        return self.usuario.username 

class UsuariosDesactivos(models.Model):
    Usuairo=models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        verbose_name='UsuarioDesactivo'
        verbose_name_plural='UsuariosDesactivos'
    def __str__ (self):
        return self.Usuairo.Nombre

