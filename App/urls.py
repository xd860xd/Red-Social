from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    
    
    path("", views.ingresar, name='ingresar'),

    path("ActualizarPerfil", views.Actualizar, name='ActualizarPerfil'),


    path("home", views.home, name='homes'),

    path("Inicio", views.Inicio, name='Inicio'),

    path("Comentario", views.Comentar, name='Comentario'),

    path("buscar", views.home, name='home'),

    path("visita/<str:usuarios>", views.visita, name='visita'),

    path("Ingresar", views.Iniciarsesion, name='Ingresar'),

    path("RegistrarUsuario", views.Registrarsed, name='RegistrarUsuario'),
    
    path("EnviarSolicitud", views.EnviarSolicitud, name='EnviarSolicitud'),
    
    path("CancelarSolicitud", views.CancelarSolicitud, name='CancelarSolicitud'),
    
    path("ProcesarSolicitud", views.ProcesarSolicitud, name='ProcesarSolicitud'),
   
    path("EliminarAmigo", views.EliminarAmigo, name='EliminarAmigo'),

    path("mensajes", views.Mensaje, name='mensajes'),
    
    path("conversacion", views.Conversacion, name='conversacion'),
    
    path("Notificaciones", views.Notificacione, name='Notificaciones'),
    
    path("Ver_Notificacion", views.Ver_Notificacion, name='Ver_Notificacion'),
    
    path("Eliminar_Notificacion", views.Eliminar_Notificacion, name='Eliminar_Notificacion'),
   
   path("me_gusta", views.Me_gusta, name='me_gusta')
]
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    
    path('chat/<str:room_name>/', views.room, name='room'),

]