from django.contrib import admin
from .models import Usuarios,UsuariosDesactivos
# Register your models here.

admin.site.register(Usuarios)

admin.site.register(UsuariosDesactivos)
