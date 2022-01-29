# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from Social.models import Mensajes
from Relaciones.models import Amigos
from Usuarios.models import Usuarios
from django.contrib.auth.models import User 
def Obtener_conversacion(id):

    amigos=Amigos.objects.get(id=id)
    amigo_1=amigos.Amigo1
    amigo_2=Usuarios.objects.get(id=amigos.Amigo2)
    
    #Cargamos todos los mnsjes entre activo & visitado    
    messages=[]
    mensajes=''
    for mensaje in Mensajes.objects.all():
        if (str(mensaje.FROM_usuario.id)==str(amigo_1.id) and str(mensaje.TO_usuario)==str(amigo_2.id)) or  (str(mensaje.FROM_usuario.id)==str(amigo_2.id) and  str(mensaje.TO_usuario)==str(amigo_1.id)):
            messages.append(mensaje)
            print(mensaje)
            mensajes+=str(mensaje.FROM_usuario.usuario.username)+' :'+str(mensaje.Mensaje)+'\n'
    return mensajes


# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        
        self.room_name = self.scope['url_route']['kwargs']['room_name']
       
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
       
        self.accept()  

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
    
    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        id_usuario= text_data_json['usuario']
        visitado=text_data_json['visitado']
        remitente=Usuarios.objects.get(usuario=User.objects.get(id=id_usuario))
        men=Mensajes(FROM_usuario=remitente, TO_usuario=visitado, Mensaje=message)
        men.save()
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': {
                    "message": message,
                    "id_usuario": id_usuario
                },
                'id_usuario' : id_usuario
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
