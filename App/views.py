#Authentication
from django.utils.decorators import method_decorator

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

#Views & Response
from django.views import View
from django.views.generic.base import RedirectView

from django.http.response import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

#Models
from Usuarios.models import Usuarios
from Social.models import Posts, Mensajes, Comentarios, Notificaciones, likes
from Relaciones.models import Amigos

#Forms
from App.forms import Registrarse,Registrarsec,Formulario, AgregarPost


class Ingresar(RedirectView):

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            return HttpResponseRedirect("Inicio")
    
        return HttpResponseRedirect('accounts/login/?next=/Inicio') #Este es un return de contraseña incorrecta
 
@method_decorator(login_required, name='dispatch')
class HomeView(View):

    def post(self, request):
       
        formulario=AgregarPost(request.POST, request.FILES)       #Si se ha creado un nuevo post

        if formulario.is_valid() and  (not Posts.objects.first() or Posts.objects.first().Descripcion !=request.POST['Descripcion']):
            formulario.save()
            return HttpResponseRedirect('Inicio')
       
        return HttpResponseRedirect('Inicio')
            
    def get(self, request):
          
        formulario=Formulario         
        
        user=User.objects.get(username=request.user)     

        array_posts = self.get_posts(user)
        
        comentarios=Comentarios.objects.all()

        cantidad_messages, cantidad_notifications = self.get_new_mss_notif(user)

        liks = self.get_likes_gave(user)

        usuario=Usuarios.objects.get(usuario=user)

        array_posts_ids = [post.id for post in array_posts]

        laikes= likes.objects.filter( user = User.objects.get(username=request.user).usuario )
        posts_likeados = [ lik.post for lik in laikes if lik.like ]


        
        return render(request, "App/Productos.html", 
                    {
                        'postslikeados':liks , 
                        'id':usuario.id, 
                        'CDM': cantidad_messages , 
                        'CDN':cantidad_notifications , 
                        'como':array_posts_ids ,
                        'comentarios': comentarios , 
                        'Posts':array_posts, 
                        'Formulario': formulario, 
                        'Author': user.usuario.id, 
                        'activos':usuario.id,
                        'postslikeados': posts_likeados
                        })


    def get_user_friends(self, user):

        array_friends=[]              #Obtenemos los amigos para obtener sus post
        friends_pairs = Amigos.objects.all()
        usuario_actual = user.usuario
        
        [array_friends.append(friends.Amigo2) for friends in friends_pairs if friends.Amigo1 == usuario_actual]
        
        return array_friends

    def get_posts(self, user):
                         
        array_posts=[]  

        for post in Posts.objects.all(): #Obtenemos los posts de los amigos   

            if post.Author.usuario == user: 
                array_posts.append(post)
               
            else:    
                [array_posts.append(post) for friend in self.get_user_friends(user) if int(post.Author.id) == int(friend)]   
        
        return array_posts

    def get_new_mss_notif(self,user):

        cantidad_notificaciones = Notificaciones.objects.filter(
            para=user.usuario.id, 
            recibido=False
            ).count()
            
        cantidad_mensajes = Mensajes.objects.filter(
            TO_usuario=user.usuario.id, 
            recibido=False
            ).count() 

        return cantidad_mensajes , cantidad_notificaciones
    
    def get_likes_gave(self, user):
        #Obtenemos los likes que hemos dado 
        usuario = user.usuario
         
        liks = [like for like in likes.objects.filter(user=usuario)  if like.like]
        
        return liks

@method_decorator(login_required, name='dispatch')
class SearchPerfilView(View):

    def get(self, request):

        user=User.objects.get(username=request.user)
        
        users=User.objects.filter( username__contains= request.GET['buscar'])

        perfiles=[]
        for usuario in users:
            try:
                perfiles.append(Usuarios.objects.get(usuario=usuario))
            except: pass    

        perfiles_busqueda = [ perfil for perfil in perfiles if perfil.usuario.id != user.id]

        return render(request, "App/home.html", {'id': user.id,'Iniciar':'Iniciar secion', 'Usuarios':perfiles_busqueda, 'activos': user})
       
 
class RegistrarseView(View):

    def post(self, request):
       
        form=Registrarse(request.POST)
        if form.is_valid(): 
            admin = Usuarios.objects.get(id = 1)

            usuario = User.objects.create_user( 
                                    username =request.POST['username'] , 
                                    email = request.POST['email'], 
                                    password = request.POST['password'], 
                                    first_name= request.POST["first_name"],  
                                    last_name= request.POST["last_name"] ) #Creacion del usuario

            login(request, usuario)

            usuario=Usuarios.objects.create(usuario= usuario)

            Amigos.objects.create(
                Amigo1=admin ,   
               
                Amigo2=usuario.id
            )      
            Amigos.objects.create(
                Amigo1=usuario ,   
               
                Amigo2=admin.id
            )           

            Mensajes.objects.create(
                Mensaje="Hey !!!, Bienvenido a mi pequeña red social, espero te guste 😜" ,
                
                FROM_usuario=admin,
                TO_usuario=usuario.id,
            )

            return HttpResponseRedirect("Inicio")

        return render(request, "App/contacto.html", {'miFormulari': form}) #Es la pagina para registrarse
    
        

    def get(self, request):
        mi_formulario=Registrarsec
        return render(request, "App/contacto.html", {'miFormulari':mi_formulario}) #Es la pagina para registrarse
    