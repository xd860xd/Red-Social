from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .routing import websocket_urlpatterns
from .views import HomeView, Ingresar, RegistrarseView, SearchPerfilView

urlpatterns = [
    path("RegistrarUsuario", RegistrarseView.as_view(), name="RegistrarUsuario"),
    path("", Ingresar.as_view(), name="ingresar"),
    path("home", SearchPerfilView.as_view(), name="homes"),
    path("Inicio", HomeView.as_view(), name="Inicio"),
    path("buscar", SearchPerfilView.as_view(), name="home"),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += websocket_urlpatterns
