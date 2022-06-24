from django.contrib import admin

# Register your models here.
from .models import Amigos, Bloqueos, Solicitudes

admin.site.register(Solicitudes)
admin.site.register(Amigos)
admin.site.register(Bloqueos)
