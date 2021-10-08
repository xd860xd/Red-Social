#Authentication
from django.utils.decorators import method_decorator

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

#Views & Response
from django.views import View

from django.http import HttpResponseRedirect
from django.shortcuts import render

#Models
from Usuarios.models import Usuarios
from Social.models import Posts, Mensajes, Comentarios, Notificaciones, likes
from Relaciones.models import Solicitudes, Amigos





# Create your views here.

      
@login_required
def Actualizar(request):
    foto=request.FILES['FOTO']
    
    activo=Usuarios.objects.get(usuario=User.objects.get(username=request.user))
    
    activo.Foto=foto
    activo.save()
    
    return HttpResponseRedirect('visita/{0}'.format(User.objects.get(username=request.user).id))

@method_decorator(login_required, name='dispatch')
class PerfilView(View):
    Visitado=None
    comodinbj=None
    V = None
    visit = None
    actf = None
    Visitado = None
    CDN = None
    CDM = None

    def post(self, request):
        user_activo = User.objects.get(username=request.user)
        usuario_activo=Usuarios.objects.get(usuario=user_activo)
        
        usuario_activo.Foto = request.FILES['FOTO']
        usuario_activo.save()
        
        return HttpResponseRedirect('visita/{0}'.format(user_activo.id))



    def get(self, request, usuarios):

        self.Visitado=usuarios  
        self.comodinobj=User.objects.get(username=request.user)
        self.V=Usuarios.objects.get(id=self.Visitado).usuario
        self.visit=Usuarios.objects.get(usuario=self.V) 

        self.actf=Usuarios.objects.get(usuario=self.comodinobj )   #Esta variable sera usada en casi todo el proceso
        self.Visitado=[ Usuarios.objects.get(id=self.Visitado)]

        #Obtenemos las cantidades de nuevos mnsjes y notificaciones
        self.CDN=Notificaciones.objects.filter(para=Usuarios.objects.get(usuario=self.actf.usuario).id, recibido=False) 
        self.CDN=self.CDN.count()
        self.CDM=Mensajes.objects.filter(TO_usuario=Usuarios.objects.get(usuario=self.actf.usuario).id, recibido=False) 
        self.CDM=self.CDM.count()



        if int(usuarios)==int(self.actf.id):#Es el perfil propio
            return self.perfil_propio(request)
                    
        try: 
            return self.perfil_amigo(request) #Es el perfil de un amigo    
        except: pass
         
        try: 
            return self.perfil_se_envio_solicitud(request)  #Se envio solicitud
        except:pass

        try: 
            return self.perfil_se_recibio_solicitud(request ) #Se recibio una solicitud de amistad

        except: 
            return self.perfil_no_hay_solicitud(request)   # No se ha enviado solicitud de amistad
            
    def perfil_no_hay_solicitud(self, request):    
        return render(request, "App/UsuarioVisitado.html", {'id':self.actf.id,'Iniciar':'Iniciar secion','Usuarios':self.Visitado, 'sol':'Enviar Solicitud de amistad', 'accion':'Enviar'})

    def perfil_se_recibio_solicitud(self, request ):
        solicitud=Solicitudes.objects.get(FROM_usuario=self.V, TO_usuario=self.actf) #Obtenemos la solicitud
        print(self.Visitado[0], "Correcto")
        return render(request, "App/UsuarioVisitado2.html", {'CDN':self.CDN,'CDM':self.CDM,'id':self.actf.id,'Iniciar':'Iniciar secion','usuario' : self.Visitado[0] , 'sol':'Enviar Solicitud de amistad', 'activos':self.actf.id, 'accion':'Enviar'})

    def perfil_se_envio_solicitud(self, request):
            
        a=User.objects.get(username=request.user) #Obtenemos el user activo
        
        pa=Usuarios.objects.get(usuario=self.V)          #Obtenemos el user visitado
         
        activo=Usuarios.objects.get(usuario=a).id   #Obtenemos el id del usuario activo
        envio=Solicitudes.objects.get(FROM_usuario=a, TO_usuario=pa) #Obtenemos la solicitud enviada
        
        return render(request, "App/UsuarioVisitado.html", {'CDN':self.CDN,'CDM':self.CDM,'id':activo,'Iniciar':'Iniciar secion','Usuarios':self.Visitado, 'sol':'Cancelar Solicitud de amistad', 'activos':activo, 'accion':'Cancelar'})

    def perfil_propio(self, request):
        posteos=Posts.objects.filter(Author=self.Visitado[0])    #obtener los post del amigo visitado
        como=[]
        for x in posteos:
            como.append(x.id)
        
        comentarios=Comentarios.objects.all()       #Obtener comentarios
       
        liks=[]                                     #Obtener liks dados
        laikes=likes.objects.filter(user=Usuarios.objects.get(usuario=self.actf.usuario))
        for lik in laikes:
            if lik.like:
                liks.append(lik.post)
           
        return render(request, "App/perfilpropio.html", {'CDN':self.CDN,'CDM':self.CDM,'id':self.actf.id,'postslikeados':liks ,'como':como, 'comentarios':comentarios,'posteos':posteos , 'Iniciar':'Iniciar secion','Usuarios':self.Visitado})

    def perfil_amigo(self, request):
            
        amistad=Amigos.objects.get(Amigo1=self.actf, Amigo2=int(Usuarios.objects.get(usuario=self.V).id)) #Obtenemos la amistad

        posteos=Posts.objects.filter(Author=Usuarios.objects.get(usuario=self.V)) #obtener los post del amigo visitado
        como=[]
        for x in posteos:
            como.append(x.id)

        comentarios=Comentarios.objects.all()       #Obtener comentarios
       
        liks=[]                                     #Obtenemos los mg que hemos dado ha sus post
        laikes=likes.objects.filter(user=self.actf)
        for lik in laikes:
            if lik.like:
                liks.append(lik.post)

        return render(request, "App/AmigoVisitado.html", {'CDN':self.CDN,'CDM':self.CDM,'id':self.actf.id ,'postslikeados':liks ,'como':como, 'comentarios':comentarios,'posteos':posteos , 'Iniciar':'Iniciar secion','Usuarios':self.Visitado, 'sol':'Enviar Solicitud de amistad' })

@method_decorator(login_required, name='dispatch')
class EliminarAmigoView(View):

    def post(self, request):

        activo=request.POST['activo']   #id
        visitado=request.POST['visitado']#id
    
        activo=Usuarios.objects.get(id=activo)
        visitado=Usuarios.objects.get(id=visitado)

        try :
            destruir=Amigos.objects.get(Amigo1=activo,Amigo2=visitado.id)
            destruir.delete()
        except: pass

        try:
            replica=Amigos.objects.get(Amigo1=visitado,Amigo2=activo.id)
            replica.delete()
        except: pass

        return HttpResponseRedirect('visita/{0}'.format(visitado.id))


@method_decorator(login_required, name='dispatch') 
class LikeView(View):


    post_actual = None
    user_activo = None
    usuario_activo = None

    def post(self, request):
       
        self.post_actual=Posts.objects.get(id=int(request.POST['postid']))
        self.user_activo=User.objects.get(username=request.user)
        self.usuario_activo = self.user_activo.usuario

        if request.POST['valor']=='1': self.dar_like_y_notificar()
            
        else: self.qutar_like()
       
        return self.retornar_interfaz(request)


    def dar_like_y_notificar(self):

        if self.usuario_activo != self.post_actual.Author:
            
            Notificaciones.objects.create(
                notificacion='Le ha gustado tu post',
                post = self.post_actual, 
                de = self.usuario_activo , 
                para = self.post_actual.Author.id)
               
        likes.objects.create(
            post=self.post_actual,
            like=True,
            user= self.usuario_activo )

        self.post_actual.me_gustas+=1
        self.post_actual.save()

    def qutar_like(self):
        
        notificacion_enviada = Notificaciones.objects.filter(   
                                    notificacion='Le ha gustado tu post', 
                                    post = self.post_actual, 
                                    de = self.usuario_activo, 
                                    para = self.post_actual.Author.id
                                    )

        like_dado = likes.objects.filter(
            
                        post=self.post_actual,
                        like=True,
                        user=self.usuario_activo
                        
                        )

        if notificacion_enviada:

            eliminar = notificacion_enviada.first()
            
            eliminar.delete()
        

        if like_dado:
            
            eliminar = like_dado.first()

            eliminar.delete()
        
            self.post_actual.me_gustas-=1
            self.post_actual.save()
            
    

    def retornar_interfaz(self, request):

        try: 
            request.POST['notificacion']
            return HttpResponseRedirect('Notificaciones')    
        except: pass

        try:
            request.POST['notificacion']
            return HttpResponseRedirect('Notificaciones')    
        except: pass

        try:
            request.POST['estaesvisita']
            return HttpResponseRedirect('visita/{0}'.format(self.post_actual.Author.id))
        except: pass

        try:
            request.POST['notificacion']
            return HttpResponseRedirect('Notificacion')       
        except: pass

        return HttpResponseRedirect('Inicio')    


@method_decorator(login_required, name='dispatch')
class ComentarView(View):

        
    def post(self, request):
        
        self.comentar(request)
        
        return self.retornar_interfaz(request)


    def comentar(self, request):

        post_id=request.POST['postId']  

        post = Posts.objects.get(id=post_id)

        user_activo = User.objects.get(username=request.user)

        usuario_activo = user_activo.usuario

        comentario = request.POST['texto']

        comentador = usuario_activo


        Comentarios.objects.create(Author=comentador, Post=post, Coment=comentario)
        
        if post.Author != comentador :

            self.notificar(comentador, post)

                
    def notificar(self, comentador, post):

        Notificaciones.objects.create(
                notificacion='Ha comentado tu post', 
                post=post, de=comentador, 
                para=int(post.Author.id)
                )


    def retornar_interfaz(self,request):

        try: 
            return HttpResponseRedirect('visita/{0}'.format(request.POST['visitado']))
        except: pass
        try:
            request.POST['notificacion']
            return HttpResponseRedirect('Notificaciones')
        except: pass
        
        try: return HttpResponseRedirect('visita/{0}'.format(request.POST['visita']))    
        except: pass
        return HttpResponseRedirect('Inicio')
        
@method_decorator(login_required, name='dispatch')
class NotificacionesView(View):

    def get(self, request):

        user_activo = User.objects.get(username= request.user  )
        usuario_activo = Usuarios.objects.get( usuario=user_activo )  
        notificaciones= Notificaciones.objects.filter( para = int(usuario_activo.id) )
        cantidad_notificaciones_pendientes = 0  
        cantidad_mensajes_pendientes = Mensajes.objects.filter(TO_usuario=usuario_activo.id, recibido=False).count()
    
                #La variable notificaciones contiene datos filtrados
    
        for notificacion in notificaciones: 
            notificacion.recibido=True
            notificacion.save()

            
        return render(request, "App/Notificaciones.html", {'id':usuario_activo.id,'CDN': cantidad_notificaciones_pendientes ,'CDM':cantidad_mensajes_pendientes ,'notificaciones':notificaciones})

    def post(self, request):

        noificacion_id = request.POST['notificacion']    
        notificacion=Notificaciones.objects.get( id= noificacion_id)

        if request.POST['funcion'] == "eliminar":
            
            notificacion.delete()
            
            return HttpResponseRedirect('Notificaciones')
        
        else:

            post=notificacion.post
            laikes= likes.objects.filter( user = User.objects.get(username=request.user).usuario )
            posts_likeados = [ lik.post for lik in laikes if lik.like ]

            user_activo=User.objects.get(username=request.user)
            return render(request, "App/Ver_Notificaciones.html", {'id':user_activo.id,'postslikeados':posts_likeados ,'notificacion':noificacion_id   ,'post':post, 'comentarios':Comentarios.objects.all()})


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })   

@method_decorator(login_required, name='dispatch')
class MessagesView(View):

    def get(self, request):
        
        user = User.objects.get(username=request.user)
        
       
        #Enlistamos los amigos para mostrarlos en el template
        usuario=Usuarios.objects.get(usuario = user)
        
        amigos=Amigos.objects.filter(Amigo2=usuario.id)
        
       
        notificaciones = Notificaciones.objects.filter(para=usuario.id, recibido=False) 
        cantidad_notificaciones = notificaciones.count()
       
        cantidad_de_mensajes = 0
        mensajes_recibidos={}
        for amigo in amigos:

            mensajes = Mensajes.objects.filter(
                                TO_usuario = usuario.id, 
                                recibido = False, 
                                FROM_usuario = Usuarios.objects.get( usuario = amigo.Amigo1.usuario )
                                )

            mensajes_recibidos[amigo]= mensajes.count()

            cantidad_de_mensajes += mensajes.count()
          
        amigos= mensajes_recibidos
                    
        return render(
            request, "App/amigos.html", 
            {
                'id':usuario.id,'M_E': mensajes_recibidos,
                'CDN':cantidad_notificaciones,
                'CDM': cantidad_de_mensajes,
                'amigos':amigos, 
                'activos':usuario.id}
                )


@method_decorator(login_required, name='dispatch')
class ConversationView(View):

    def is_message_in_conversation(self,mensaje, usuario_activo, id_usuario_visitado):
        return (
            (
                str(mensaje.FROM_usuario.id) == str(usuario_activo.id) and 
                str(mensaje.TO_usuario) == str(id_usuario_visitado)
                ) 
                or 
            (
                str(mensaje.FROM_usuario.id)==str(id_usuario_visitado) and 
                str(mensaje.TO_usuario)==str(usuario_activo.id)
                )
            )
  

    def get(self, request):

       
        #user_activo = request.user
    
        id_usuario_visitado=request.GET['visitado']              

        usuario_activo = request.user.usuario

        all_messages =  Mensajes.objects.all()

        messages_of_conversation = [ mensaje for mensaje in all_messages if self.is_message_in_conversation( mensaje, usuario_activo, id_usuario_visitado) ]
        
        CDM=all_messages.filter(TO_usuario= usuario_activo.id, recibido=False) 
        CDM=CDM.count()
        CDN=Notificaciones.objects.filter(para=usuario_activo.id, recibido=False) 
        CDN=CDN.count()

        messages_of_conversation=messages_of_conversation[-4 : ]
        return render(request, "App/mensajes.html", {'id': usuario_activo.id,'CDN':CDN, 'CDM':CDM,'mensajes':messages_of_conversation, 'visitado': id_usuario_visitado, 'activos': request.user})


    def post(self, request):

        usuario_activo = request.user.usuario

        id_usuario_visitado=request.POST['visitado']              

        texto = request.POST['texto'] #Es el texto de mnsj

        Mensajes.objects.create(
                    Mensaje=texto, 
                    FROM_usuario= usuario_activo, 
                    TO_usuario = id_usuario_visitado) 

        return HttpResponseRedirect("conversacion?visitado="+id_usuario_visitado)
    
                    