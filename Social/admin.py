from django.contrib import admin

# Register your models here.
from .models import (
    Comentarios,
    ComentariosActivos,
    ComentariosDesactivos,
    Mensajes,
    MensajesActivos,
    MensajesDesactivos,
    Notificaciones,
    Posts,
    PostsActivos,
    PostsDesactivos,
)

admin.site.register(Posts)
admin.site.register(PostsActivos)
admin.site.register(PostsDesactivos)

admin.site.register(Comentarios)
admin.site.register(ComentariosActivos)
admin.site.register(ComentariosDesactivos)

admin.site.register(Mensajes)
admin.site.register(MensajesActivos)
admin.site.register(MensajesDesactivos)

admin.site.register(Notificaciones)
