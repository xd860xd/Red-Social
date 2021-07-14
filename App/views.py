from django.shortcuts import render
from .forms import FormularioContacto, Registrarse,Registrarsec,Formulario, AgregarPost
from Usuarios.models import Usuarios
from Social.models import Posts, Mensajes, Comentarios, Notificaciones, likes
from Relaciones.models import Solicitudes, Amigos
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth import login
import datetime
# Create your views here.

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })   


def ingresar(request):
    formulario_de_inicio_de_secion=FormularioContacto
    Formulario_de_registro=Registrarsec
    if request.user.is_authenticated:
        return HttpResponseRedirect("Inicio")
    
    return HttpResponseRedirect('accounts/login/?next=/Inicio') #Este es un return de contraseña incorrecta
       
@login_required
def Actualizar(request):
    foto=request.FILES['FOTO']
    
    activo=Usuarios.objects.get(usuario=User.objects.get(username=request.user))
    
    activo.Foto=foto
    activo.save()
    
    return HttpResponseRedirect('visita/{0}'.format(User.objects.get(username=request.user).id))

@login_required
def Inicio(request):
    Formulari=Formulario            #Este formulario es para crear un post
     
    form=AgregarPost(request.POST, request.FILES)       #Si se ha creado un nuevo post
    if form.is_valid() and Posts.objects.first().Descripcion !=request.POST['Descripcion']:
        form.save()
        return HttpResponseRedirect('Inicio')
        
    else:   #Se cliko en el boton de inicio
        
        Us=User.objects.get(username=request.user)          #Obtenemos el user

        arry=[]                 #Obtenemos los amigos para obtener sus post
        for Am in Amigos.objects.all():
            if str(Am.Amigo1.usuario.username)==str(Us.username):
                arry.append(Am.Amigo2)

        como=[]                           
        arreglo=[]  
        for pos in Posts.objects.all(): #Obtenemos los posts de los amigos   
            if str(pos.Author.usuario)==str(Us):
                arreglo.append(pos)
                como.append(pos.id)
            else:    
                for arr in arry:
                    if int(pos.Author.id)==int(arr):
                        arreglo.append(pos)
                        como.append(pos.id)

        comentarios=Comentarios.objects.all() #Obtenemos comentarios

        #Obtenemos las cantidades de nuevos mnsjs y notificacione
        CDN=Notificaciones.objects.filter(para=Usuarios.objects.get(usuario=Us).id, recibido=False) 
        CDN=CDN.count()
        CDM=Mensajes.objects.filter(TO_usuario=Usuarios.objects.get(usuario=Us).id, recibido=False) 
        CDM=CDM.count()

        liks=[]        #Obtenemos los likes que hemos dado 
        actf=Usuarios.objects.get(usuario=Us)
        laikes=likes.objects.filter(user=actf)
        for lik in laikes:
            if lik.like:
                liks.append(lik.post)

        return render(request, "App/Productos.html", {'postslikeados':liks , 'id':actf.id, 'CDM':CDM , 'CDN':CDN , 'como':como ,'comentarios': comentarios , 'Posts':arreglo, 'Formulario': Formulari, 'Author': Usuarios.objects.get(usuario=Us).id, 'activos':actf.id})
    
def Me_gusta(request):
    print("Hasta aqui todo bien")
    post=Posts.objects.get(id=int(request.POST['postid']))
    usua=User.objects.get(username=request.user)
    if request.POST['valor']=='1':
        if usua != post.Author.usuario:
            noti=Notificaciones(notificacion='Le ha gustado tu post', post=post, de=Usuarios.objects.get(usuario=usua),para=post.Author.id) #AQUI PARA SER PRECISO
            noti.save()
        a=likes(post=post,like=True,user=Usuarios.objects.get(usuario=usua))
        a.save()
        post.me_gustas+=1
        post.save()
        
    else: 
        try:
            noti=Notificaciones.objects.get(notificacion='Le ha gustado tu post', post=post, de=Usuarios.objects.get(usuario=usua),para=post.Author.id)
            noti.delete()
        except: comodin=0
        a=likes.objects.get(post=post,like=True,user=Usuarios.objects.get(usuario=usua))
        a.delete() 
        post.me_gustas-=1
        post.save()
    print("Hasta aqui todo bien")
    try: 
        try:
            print(request.POST['notificacion'])
            return HttpResponseRedirect('Notificaciones')    
        except:
            print(999999999999999999)
            print(request.POST['estaesvisita']) 
            return HttpResponseRedirect('visita/{0}'.format(post.Author.id))
    except:  
        try:
            print(request.POST['notificacion'])
            return HttpResponseRedirect('Notificacion')    
        except: return HttpResponseRedirect('Inicio')    

def home(request): 
    try:
        print(46767)
        print(000000000000000000000000000000000000000)
        activo=User.objects.get(username=request.user)
        activo=activo.id
        buscador=request.POST['buscar']
        arreglo=[]
        print(11111111111111111111111111111111111111111111)
        
        usuar=User.objects.filter(username__contains=buscador)
        print(usuar)
        s=[]
        for usu in usuar:
            try:
                wr=Usuarios.objects.get(usuario=usu)
                
                s.append(wr)
            except: pass    
        usuar=s
        #usuar=Usuairos.objects.filter(usuario__username__contains=q)
        print(11111111111111111111111111111111111111111111)
        for W in usuar:
            print('!!!!')
            if str(W.usuario.id)!=activo:
                arreglo.append(W)

        print(222222222222222222222222222222222222222222222)
        print(usuar) 
        activo=User.objects.get(id=activo) 
        
        print(activo)  
        print(arreglo)

        return render(request, "App/home.html", {'id':activo.id,'Iniciar':'Iniciar secion', 'Usuarios':arreglo, 'activos': activo.id})
    except:
        print("Error--------------------------------")
        return render(request, "App/home.html", {'Iniciar':'Iniciar secion'})

def Iniciarsesion(request):
    m=FormularioContacto
    ma=Registrarsec
    print("________________")
    print(ma)
    return render(request, "App/contacto.html", {'miFormulario':m, 'miFormulari':ma})
 
def Registrarsed(request):
    mi_formulario=Registrarsec
    if request.method=='POST': #Este es el procedimiento para crear un usuario
        form=Registrarse(request.POST)
        if form.is_valid():

            username=request.POST['username']   #En esta parte recolectamos los datos del formulario
            email=request.POST['email']
            password=request.POST['password']
            name=request.POST['first_name']
            last_name=request.POST['last_name']
            
            nuevo_usuario=User.objects.create_user( username , email, password ) #Creacion del usuario
            nuevo=User.objects.last()
            nuevo.first_name=name
            nuevo.last_name=last_name
            nuevo.save()

            p=User.objects.last()
            j=Usuarios(usuario=p)
            j.save()
            login(request, p)
            return HttpResponseRedirect("Inicio")

        else: pass
    return render(request, "App/contacto.html", {'miFormulari':mi_formulario}) #Es la pagina para registrarse
 
@login_required        
def visita(request, usuarios): #Es el id del usuario

    Visitado=usuarios  
    comodinobj=User.objects.get(username=request.user)
    V=Usuarios.objects.get(id=Visitado).usuario
    visit=Usuarios.objects.get(usuario=V) 

    actf=Usuarios.objects.get(usuario=comodinobj )   #Esta variable sera usada en casi todo el proceso
    Visitado=[ Usuarios.objects.get(id=Visitado)]

    #Obtenemos las cantidades de nuevos mnsjes y notificaciones
    CDN=Notificaciones.objects.filter(para=Usuarios.objects.get(usuario=actf.usuario).id, recibido=False) 
    CDN=CDN.count()
    CDM=Mensajes.objects.filter(TO_usuario=Usuarios.objects.get(usuario=actf.usuario).id, recibido=False) 
    CDM=CDM.count()

    if int(usuarios)==int(actf.id):#Es el perfil propio
        
        posteos=Posts.objects.filter(Author=Visitado[0])    #obtener los post del amigo visitado
        como=[]
        for x in posteos:
            como.append(x.id)
        
        comentarios=Comentarios.objects.all()       #Obtener comentarios
       
        liks=[]                                     #Obtener liks dados
        laikes=likes.objects.filter(user=Usuarios.objects.get(usuario=actf.usuario))
        for lik in laikes:
            if lik.like:
                liks.append(lik.post)
           
        return render(request, "App/perfilpropio.html", {'CDN':CDN,'CDM':CDM,'id':actf.id,'postslikeados':liks ,'como':como, 'comentarios':comentarios,'posteos':posteos , 'Iniciar':'Iniciar secion','Usuarios':Visitado})

    try: #ES AMiGO
        amistad=Amigos.objects.get(Amigo1=actf, Amigo2=int(Usuarios.objects.get(usuario=V).id)) #Obtenemos la amistad

        posteos=Posts.objects.filter(Author=Usuarios.objects.get(usuario=V)) #obtener los post del amigo visitado
        como=[]
        for x in posteos:
            como.append(x.id)

        comentarios=Comentarios.objects.all()       #Obtener comentarios
       
        liks=[]                                     #Obtenemos los mg que hemos dado ha sus post
        laikes=likes.objects.filter(user=actf)
        for lik in laikes:
            if lik.like:
                liks.append(lik.post)

        return render(request, "App/AmigoVisitado.html", {'CDN':CDN,'CDM':CDM,'id':actf.id ,'postslikeados':liks ,'como':como, 'comentarios':comentarios,'posteos':posteos , 'Iniciar':'Iniciar secion','Usuarios':Visitado, 'sol':'Enviar Solicitud de amistad' })

    except: pass
        
    try: #Se envio solicitud
       
        a=User.objects.get(username=request.user) #Obtenemos el user activo
        
        pa=Usuarios.objects.get(usuario=V)          #Obtenemos el user visitado
         
        activo=Usuarios.objects.get(usuario=a).id   #Obtenemos el id del usuario activo
        envio=Solicitudes.objects.get(FROM_usuario=a, TO_usuario=pa) #Obtenemos la solicitud enviada
        
        return render(request, "App/UsuarioVisitado.html", {'CDN':CDN,'CDM':CDM,'id':activo,'Iniciar':'Iniciar secion','Usuarios':Visitado, 'sol':'Cancelar Solicitud de amistad', 'activos':activo, 'accion':'Cancelar'})

    except:pass

    try: #Se recibio una solicitud de amistad
        solicitud=Solicitudes.objects.get(FROM_usuario=V, TO_usuario=actf) #Obtenemos la solicitud
        
        sol1='Aceptar Solicitud'    #Establecemos cadenas para accionar en el formulario
        sol2='Rechazar solicitud'
        
        return render(request, "App/UsuarioVisitado2.html", {'CDN':CDN,'CDM':CDM,'id':actf.id,'Iniciar':'Iniciar secion','Usuarios':Visitado, 'sol':'Enviar Solicitud de amistad', 'activos':actf.id, 'accion':'Enviar'})

    except:    # No se ha enviado solicitud de amistad
        return render(request, "App/UsuarioVisitado.html", {'id':actf.id,'Iniciar':'Iniciar secion','Usuarios':Visitado, 'sol':'Enviar Solicitud de amistad', 'accion':'Enviar'})

@login_required
def EnviarSolicitud(request):
    activo=User.objects.get(username=request.user).id   #Es el id del User
    visitado=request.POST['visitado'] #Es el id del Usuario
    vai=visitado
    print(activo)
    print(vai)
    
    print("--------------------------------------------------------------------------------------------")
    pas=request.POST['pass']
    
    Visitado=Usuarios.objects.get(id=request.POST['visitado']) #Debe ded ser usuario
    
    Activo=User.objects.get(username=request.user)

    j=Solicitudes(Envio=True, FROM_usuario=Activo, Recibio=False, TO_usuario=Visitado)
    j.save()
    k=Notificaciones(notificacion='Te ha enviado una solicitud de amistad', solicitud=j, de=Usuarios.objects.get(usuario=Activo), para=Visitado.id)
    k.save()
    return HttpResponseRedirect('visita/{0}'.format(vai))
    return render(request, "App/UsuarioVisitado.html",{'id':Activo.id,'Iniciar':'Iniciar secion','Usuarios':Visitado1, 'sol':'Cancelar Solicitud de amistad', 'activo':activo, 'accion':'Cancelar', 'activos': activo})

@login_required
def CancelarSolicitud(request):
    activo=User.objects.get(username=request.user).id   #Se resibe el id del User
    visitado=request.POST['visitado'] #Se recibe el id del User
    vai=visitado
    Activo=User.objects.get(username=request.user)
    Visitado=Usuarios.objects.get(id=request.POST['visitado'])
    print(Visitado)
    j=Solicitudes.objects.get(FROM_usuario=Activo, TO_usuario=Visitado)
    j.delete()

    return HttpResponseRedirect('visita/{0}'.format(vai))

    return render(request, "App/UsuarioVisitado.html",{'id':Activo.id,'Iniciar':'Iniciar secion','Usuarios':Visitado1, 'sol':'Enviar Solisitud de amistad', 'activo':activo, 'accion':'Enviar', 'activos': activo})
@login_required
def ProcesarSolicitud(request):
    activo=User.objects.get(username=request.user)
    activo=activo.id
    #activo=request.POST['activo']       #Debe de ser el id el parametro recibido
    visitado11=request.POST['visitado']   #El id es del usuario 
    print(activo)
    print(visitado11)
    
    #En esta parte obtenemos los objetos User del act & el vis
    activo=Usuarios.objects.get(usuario=User.objects.get(id=activo))
    visitado=Usuarios.objects.get(id=visitado11)
    print('----------------------------Obtencion de usuarios correcta--------------------------')
    activof=Usuarios.objects.get(usuario=activo.usuario)   #Aqui obtenemos el usuario
    if request.POST['solicitud']=='Aceptar':
        print(User.objects.get(id=visitado11))
        print(activof.usuario)

        destruir=Solicitudes.objects.get(FROM_usuario=visitado.usuario, TO_usuario=activof)
        destruir.delete()
 
        crear=Amigos(Amigo1=Usuarios.objects.get(usuario=visitado.usuario), Amigo2=activo.id)
        crear.save()
        replica=Amigos(Amigo1=Usuarios.objects.get(usuario=activo.usuario), Amigo2=visitado.id)
        replica.save()

    else:
        destruir=Solicitudes.objects.get(FROM_usuario=visitado.usuario, TO_usuario=activof)
        destruir.delete()
    try:
        a=request.POST['pass']
        
        print("___________________________________AAAAAAAAAARRRRRRRRREEEEEEEEEAAAAAAAAAA_________________")
        Visitado=request.POST['visitado']
        activo=request.POST['activo']
        
        V=User.objects.get(username=Visitado)
        visit=Usuarios.objects.get(Usuairo=V)

        act=User.objects.get(username=activo)
        actf=Usuarios.objects.get(usuario=act)

        print(Visitado)
        Visitado=[User.objects.get(username=Visitado)]
        print("La consulta es correcta")
        return render(request, "App/UsuarioVisitado.html", {'Iniciar':'Iniciar secion','Usuarios':Visitado, 'sol':'Enviar Solicitud de amistad', 'activos':activo, 'accion':'Enviar'})


    except: 
        try: 
            print(request.POST['notificacion'])
            return HttpResponseRedirect("Notificaciones")
        except:
            return HttpResponseRedirect("Inicio")
           
@login_required
def EliminarAmigo(request):
    activo=request.POST['activo']   #id
    visitado=request.POST['visitado']#id
    print(visitado)
    print("------------------------------------------------oooooooooooooooo........------------------")
    activo=Usuarios.objects.get(id=activo)
    visitado=Usuarios.objects.get(id=visitado)

    destruir=Amigos.objects.get(Amigo1=activo,Amigo2=visitado.id)
    destruir.delete()

    replica=Amigos.objects.get(Amigo1=visitado,Amigo2=activo.id)
    replica.delete()
    Visitado=[visitado]
    print(visitado)
    print("La consulta es correcta")
    return render(request, "App/UsuarioVisitado.html", {'id':activo.id,'Iniciar':'Iniciar secion','Usuarios':Visitado, 'sol':'Enviar Solicitud de amistad', 'activos':activo.id, 'accion':'Enviar'})

@login_required
def Mensaje(request):
    
    print("MEnsajes")
    #Se clickeo en el boton mensajes   <--------------
    activo=User.objects.get(username=request.user)
    
    print(activo)
    #Enlistamos los amigos para mostrarlos en el template
    Usuario=Usuarios.objects.get(usuario=activo)
    
    amigos=Amigos.objects.filter(Amigo2=Usuario.id)
    print(amigos)
    

    CDM=Mensajes.objects.filter(TO_usuario=Usuario.id, recibido=False) 
    CDM=CDM.count()
    print(0)
    CDN=Notificaciones.objects.filter(para=Usuario.id, recibido=False) 
    CDN=CDN.count()
    print(1)
    M_E={}
    for amigo in amigos:
       M_E[amigo]=Mensajes.objects.filter(TO_usuario=Usuario.id, recibido=False, FROM_usuario=Usuarios.objects.get(usuario=amigo.Amigo1.usuario)).count()
    print(2)
    amigos=M_E
    print(amigos)
    for amigo in amigos:
        print(amigos[amigo])
        
    Usuario=Usuario       
    return render(request, "App/amigos.html", {'id':Usuario.id,'M_E':M_E,'CDN':CDN,'CDM':CDM,'amigos':amigos, 'activos':Usuario.id})

@login_required
def Conversacion(request):

    activo=User.objects.get(username=request.user) #Obtenemos el ussr activo
    visitado=request.POST['visitado']               #Obtenemos el usuario_id del visitado
    
    amistad=Amigos.objects.get(Amigo1=Usuarios.objects.get(usuario=request.user), Amigo2=visitado).id
    amistad2=Amigos.objects.get(Amigo1=Usuarios.objects.get(id=visitado), Amigo2=Usuarios.objects.get(usuario=request.user).id).id
    if amistad>amistad2:
        am=amistad2
    else: am=amistad    
    
    print(amistad)

    CDM=Mensajes.objects.filter(TO_usuario=Usuarios.objects.get(usuario=activo).id, recibido=False) 
    CDM=CDM.count()
    CDN=Notificaciones.objects.filter(para=Usuarios.objects.get(usuario=activo).id, recibido=False) 
    CDN=CDN.count()


    return render(request, 'App/mensajes.html', {
        'room_name': am,
        'usuario':str(request.user),
        'visitado':visitado,
        'id':Usuarios.objects.get(usuario=activo).id,
        'CDN':CDN, 
        'CDM':CDM,
        
        'activos':activo})


    activo=User.objects.get(username=request.user) #Obtenemos el ussr activo
    visitado=request.POST['visitado']               #Obtenemos el usuario_id del visitado
    
    try:  # Mandamos el mensaje si existe
        de=Usuarios.objects.get(usuario=User.objects.get(username=request.user)) #Es el que envia
        error=Mensajes.objects.filter(TO_usuario=visitado, FROM_usuario=de) #Es el mnsj anterior para no enviar de nuevo si la pag reacarga
        texto=request.POST['texto']                             #Es el texto de mnsj
        
        if error:   #Si no es el primer mensaje
            error=error[0]                              #Si el ultimo mnsj es distinto del actual se envia el mnsj
            if texto!=str(error.Mensaje):
                ms=Mensajes(Mensaje=texto, FROM_usuario=de, TO_usuario=visitado)
                ms.save()
        else: #Si es el primer mnsj 
            ms=Mensajes(Mensaje=texto, FROM_usuario=de, TO_usuario=visitado)
            ms.save()        

    except:pass  

    #Cargamos todos los mnsjes entre activo & visitado    
    messages=[]
    for mensaje in Mensajes.objects.all():
        if (str(mensaje.FROM_usuario.id)==str(Usuarios.objects.get(usuario=activo).id) and str(mensaje.TO_usuario)==str(visitado)) or (str(mensaje.FROM_usuario.id)==str(visitado) and str(mensaje.TO_usuario)==str(Usuarios.objects.get(usuario=activo).id)):
            messages.append(mensaje)
            
    #Actualizamos la bandeja de entrada
    for act in Mensajes.objects.filter(TO_usuario=Usuarios.objects.get(usuario=activo).id, recibido=False, FROM_usuario_id=visitado):
        act.recibido=True
        act.save()
        
    #Obtenemos los nuevos mnsgs y notificaciones    
    CDM=Mensajes.objects.filter(TO_usuario=Usuarios.objects.get(usuario=activo).id, recibido=False) 
    CDM=CDM.count()
    CDN=Notificaciones.objects.filter(para=Usuarios.objects.get(usuario=activo).id, recibido=False) 
    CDN=CDN.count()
   
    return render(request, "App/mensajes.html", {'id':Usuarios.objects.get(usuario=activo).id,'CDN':CDN, 'CDM':CDM,'mensajes':messages, 'visitado':visitado, 'activos':activo})

@login_required    
def Comentar(request):
    
    Formulari=Formulario
    postID=request.POST['postId']  
    activo=request.POST['activos']  #Debe ser un id
    coment=request.POST['texto']
    author=Usuarios.objects.get(usuario=User.objects.get(username=request.user))  #Obtenemos el user con el id activo
    post=Posts.objects.get(id=postID)
    error=Comentarios.objects.first()
    if error == None or (str(error.Coment)!=coment or str(error.Author.id)!=activo):
        nuevo=Comentarios(Author=author, Post=post, Coment=coment)
        nuevo.save()
        if int(post.Author.id) != int(author.id):
            notif=Notificaciones(notificacion='Ha comentado tu post', post=post, de=author, para=int(post.Author.id))
            notif.save()
    #Recargar la pagina xc

   # Usu=request.POST['Nombre_Usuario']
    print("---------------------------------INICIO-------------------------------3")

    try: #Esta try es por si estamos de visita en un perfil retornemos en la misma vista de visita
        return HttpResponseRedirect('visita/{0}'.format(request.POST['visitado']))
        
    except: #Este ecxept es la pagina de inicio o del template de las notificaciones
        try:
            print(request.POST['notificacion'])
            return HttpResponseRedirect('Notificaciones')

        except: 

            try: return HttpResponseRedirect('visita/{0}'.format(request.POST['visita'])) 
                
            except: return HttpResponseRedirect('Inicio')
     
@login_required
def Notificacione(request):
        
    usern=request.user    
    Us=User.objects.get(username=usern)
    Us=Usuarios.objects.get(usuario=Us)
    notificaciones=[]         #Filtramos las notificaciones
    for noti in Notificaciones.objects.all():
        if int(noti.para) == int(Us.id):
            notificaciones.append(noti)
            #La variable notificaciones contiene datos filtrados
    print(Us.id)
    CDN=Notificaciones.objects.filter(para=Us.id, recibido=False) 
   
    for c in CDN:
        c.recibido=True
        c.save()
    CDN=0    
    CDM=Mensajes.objects.filter(TO_usuario=Us.id, recibido=False) 
    CDM=CDM.count()      
    
    return render(request, "App/Notificaciones.html", {'id':Us.id,'CDN':CDN,'CDM':CDM ,'notificaciones':notificaciones})

@login_required
def Ver_Notificacion(request):
    #Aqui tenemos que obtener todos los atributos del objeto notificacion
    id_noti=request.POST['notificacion']    
    notificacion=Notificaciones.objects.get(id=id_noti)
    post=notificacion.post

    liks=[]                                     #Obtener liks dados
    laikes=likes.objects.filter(user=Usuarios.objects.get(usuario=User.objects.get(username=request.user)))
    for lik in laikes:
        if lik.like:
            liks.append(lik.post)

    print(liks)
    Us=User.objects.get(username=request.user)
    return render(request, "App/Ver_Notificaciones.html", {'id':Us.id,'postslikeados':liks ,'notificacion':id_noti ,'post':post, 'comentarios':Comentarios.objects.all()})

def Eliminar_Notificacion(request):
    #Aqui tenemos que obtener todos los atributos del objeto notificacion
    id_noti=request.POST['notificacion']    
    notificacion=Notificaciones.objects.get(id=id_noti)
    notificacion.delete()
    return HttpResponseRedirect('Notificaciones')
