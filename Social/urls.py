from .views import *
from django.urls import path

urlpatterns = [
    
    path("visita/<str:usuarios>", PerfilView.as_view(), name='visita'),

    path("ActualizarPerfil", PerfilView.as_view(), name='ActualizarPerfil'),

    path("EliminarAmigo", EliminarAmigoView.as_view(), name='EliminarAmigo'),
   
    path("Notificaciones", NotificacionesView.as_view(), name='Notificaciones'),
    
    path("Ver_Notificacion", NotificacionesView.as_view(), name='Ver_Notificacion'),
    
    path("Eliminar_Notificacion", NotificacionesView.as_view(), name='Eliminar_Notificacion'),
   
    path("me_gusta", LikeView.as_view(), name='me_gusta'),

    path("Comentario", ComentarView.as_view(), name='Comentario'),

    path("mensajes", MessagesView.as_view(), name='mensajes'),
    
    path("conversacion", ConversationView.as_view(), name='conversacion'),

]


urlpatterns += [
    
    path('chat/<str:room_name>/', room, name='room'),

]