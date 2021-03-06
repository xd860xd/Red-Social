from django import forms
from django.contrib.auth.models import User

from Social.models import Posts


class FormularioContacto(forms.Form):

    User_name = forms.CharField(label="Usuario", required=True)

    Password = forms.CharField(widget=forms.PasswordInput())


class Registrarse(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]


class Registrarsec(forms.Form):

    username = forms.CharField(label="Nombre de Usuario", required=True)
    first_name = forms.CharField(label="Nombre", required=True)
    last_name = forms.CharField(label="Apellido", required=True)
    email = forms.EmailField(label="Correo Electronico")
    password = forms.CharField(widget=forms.PasswordInput())


class Formulario(forms.Form):

    Nombre = forms.CharField(label="Nombre", required=True)
    Descripcion = forms.CharField(widget=forms.Textarea(attrs={"filas": 2, "cols": 20}))
    Foto = forms.ImageField(label="Imagen", required=True)


class AgregarPost(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ["Nombre", "Descripcion", "Foto", "Author"]
