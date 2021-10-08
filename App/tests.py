from django.test import TestCase

# Create your tests here.

class TestViewsHome(TestCase):

    def setUp(self) -> None:

        self.data_nuevo_registro = {

            "username" : "admin" , 
            "email" : "prueba@dhj.dj", 
            "password": "12345",
            "first_name": "jhkas", 
            "last_name" : "kjhda"

        }

        self.data_usuario_de_prueba = {

            "username" : "usuario_prueba" , 
            "email" : "prueba@dhqj.dj", 
            "password": "12345",
            "first_name": "jhkas", 
            "last_name" : "kjhda"

        }
        self.usuario_de_prueba = self.client.post("https://redsocialxd.herokuapp.com/RegistrarUsuario", self.data_usuario_de_prueba)

        self.client.post("https://redsocialxd.herokuapp.com/accounts/logout/?next=/")



        return super().setUp()

    def test_registrarse(self):
        
        response= self.client.post("https://redsocialxd.herokuapp.com/RegistrarUsuario", self.data_nuevo_registro)

        self.assertEqual(response.status_code, 302)

    def test_login(self):

        response= self.client.post("https://redsocialxd.herokuapp.com/accounts/login/?next=/", self.data_usuario_de_prueba)

        self.assertEqual(response.status_code, 302)

    def test_crear_posts(self):

        response= self.client.post("https://redsocialxd.herokuapp.com/Inicio", self.data_usuario_de_prueba)

        self.assertEqual(response.status_code, 302)

    