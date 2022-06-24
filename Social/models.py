from django.db import models

from Relaciones.models import Solicitudes
from Usuarios.models import Usuarios

# Create your models here.


class Posts(models.Model):
    Nombre = models.CharField(max_length=50)
    Descripcion = models.TextField(max_length=1000, null=True)
    Foto = models.ImageField(upload_to="Posts", null=True, blank=True)
    Author = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    me_gustas = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ["-created"]

    def __str__(self):
        return self.Nombre


class PostsActivos(models.Model):
    Post = models.ForeignKey(Posts, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "PostActivo"
        verbose_name_plural = "PostsActivos"

    def __str__(self):
        return self.Post.Nombre


class PostsDesactivos(models.Model):
    Post = models.ForeignKey(Posts, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "PostDesactivo"
        verbose_name_plural = "PostsDesactivos"

    def __str__(self):
        return self.Post.Nombre


class Comentarios(models.Model):
    Coment = models.CharField(max_length=50)
    Foto = models.ImageField(upload_to="Comentarios", null=True, blank=True)
    Post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    Author = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"
        ordering = ["-created"]

    def __str__(self):
        return self.Coment


class ComentariosActivos(models.Model):
    Comentario = models.ForeignKey(Comentarios, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "ComentarioActivo"
        verbose_name_plural = "ComentariosActivos"

    def __str__(self):
        return self.Post.Nombre


class ComentariosDesactivos(models.Model):
    Comentario = models.ForeignKey(Comentarios, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "ComentarioDesactivo"
        verbose_name_plural = "ComentariosDesactivos"

    def __str__(self):
        return self.Post.Nombre


class Mensajes(models.Model):
    Mensaje = models.CharField(max_length=1000)
    Foto = models.ImageField(upload_to="Mensajes", null=True, blank=True)
    FROM_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    TO_usuario = models.IntegerField(null=False)  # Este es el Usuario id del amigo
    created = models.DateTimeField(auto_now_add=True)
    recibido = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Mensaje"
        verbose_name_plural = "Mensajes"
        ordering = ["created"]

    def __str__(self):
        return self.Mensaje


class MensajesActivos(models.Model):
    Mensaje = models.ForeignKey(Mensajes, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "MensajeActivo"
        verbose_name_plural = "MensajesActivos"

    def __str__(self):
        return self.Mensaje.Mensaje


class MensajesDesactivos(models.Model):
    Mensaje = models.ForeignKey(Mensajes, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "MensajeDesctivo"
        verbose_name_plural = "MensajesDesactivos"

    def __str__(self):
        return self.Mensaje.Mensaje


class Notificaciones(models.Model):
    notificacion = models.CharField(max_length=100)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, null=True)
    solicitud = models.ForeignKey(Solicitudes, on_delete=models.CASCADE, null=True)
    de = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    img_de = models.ImageField(upload_to="Notificaciones", null=True, blank=True)
    para = models.IntegerField()  # Es el id del user del notificado
    fecha = models.DateTimeField(auto_now_add=True)
    recibido = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Notificacion"
        verbose_name_plural = "Notificiones"
        ordering = ["-fecha"]

    def __str__(self):
        return self.notificacion


class likes(models.Model):
    like = models.BooleanField(default=False)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
