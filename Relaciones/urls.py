from django.urls import path
from .views import *

urlpatterns = [

    path("EnviarSolicitud",EnviarSolicitudView.as_view(), name='EnviarSolicitud'),
    
    path("CancelarSolicitud",EnviarSolicitudView.as_view(), name='CancelarSolicitud'),
    
    path("ProcesarSolicitud",ProcesarSolicitudView.as_view(), name='ProcesarSolicitud'),
   
]