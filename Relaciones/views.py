#Authentication
from django.utils.decorators import method_decorator

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

#Views & Response
from django.views import View

from django.http import HttpResponseRedirect
from django.shortcuts import render

#Models
from Usuarios.models import Usuarios
from Social.models import Notificaciones
from Usuarios.models import Usuarios
from Social.models import Notificaciones
from Relaciones.models import Solicitudes, Amigos


@method_decorator(login_required, name='dispatch')
class EnviarSolicitudView(View):

    
    def post(self, request):
        user_activo=User.objects.get(username=request.user) 
        usuario_visitado_id =request.POST['visitado'] 
        usuario_visitado=Usuarios.objects.get(id = usuario_visitado_id)
        if request.POST['funcion'] == "Cancelar":

            solicitud_a_eliminar = Solicitudes.objects.get(FROM_usuario = user_activo, TO_usuario = usuario_visitado)
            solicitud_a_eliminar.delete()

        else :
            print("Validacion 1")
            solicitud=Solicitudes(Envio=True, FROM_usuario= user_activo, Recibio=False, TO_usuario = usuario_visitado)
            solicitud.save()
            print("Validacion 2")
            notificacion = Notificaciones(notificacion='Te ha enviado una solicitud de amistad', solicitud=solicitud, de = user_activo.usuario, para=usuario_visitado.id)
            notificacion.save()
            print("Validacion 3")
        
        return HttpResponseRedirect('visita/{0}'.format(usuario_visitado_id))
            
@method_decorator(login_required, name='dispatch')
class ProcesarSolicitudView(View):

    def post(self, request):
        activo=User.objects.get(username=request.user)
    
        usuario_activo=Usuarios.objects.get(usuario=activo)
        
        visitado_usuario_id=request.POST['visitado']  
        
        usuario_visitado=Usuarios.objects.get(id=visitado_usuario_id)
    
        
        if request.POST['solicitud']=='Aceptar':
            
            print(usuario_activo)

            print(usuario_visitado)

            print(usuario_visitado.usuario)
    
            crear=Amigos(Amigo1=usuario_visitado, Amigo2=usuario_activo.id)
            crear.save()
            replica=Amigos(Amigo1=usuario_activo, Amigo2=usuario_visitado.id)
            replica.save()

        solicitud_a_destruir=Solicitudes.objects.get(FROM_usuario=usuario_visitado.usuario, TO_usuario=usuario_activo)
        solicitud_a_destruir.delete()

        try:
            request.POST['devisita']
            return HttpResponseRedirect("visita/"+ visitado_usuario_id )
        
        except: pass

        try: 
            request.POST['notificacion']
            return HttpResponseRedirect("Notificaciones")
        except:
            return HttpResponseRedirect("Inicio")
        