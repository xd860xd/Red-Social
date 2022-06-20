from django.contrib.auth.models import User

from Usuarios.models import Usuarios
from django.db import migrations


def create_superuser(apps, schema_editor):

    Usarios = apps.get_model('Usuarios', "Usuarios")

    users = User.objects.filter(is_superuser = True)
    for user in users:

        Usuarios.objects.create(usuario= user)

    if not users.exists():
        data_admin = {
            "username": "admin",
            "name": "admin",
            "last_name": "admin",
            "email": "admin@admin.com"
            }

        user = User.objects.create(**data_admin)

        Usuarios.objects.create(usuario = user)



class Migration(migrations.Migration):





    dependencies = [
        ('Usuarios', '0001_initial'),
    ]

    operations = [ migrations.RunPython(create_superuser)
    ]
