from django.urls import path
from  .views import *

urlpatterns = [
    path("listar_clientes", listar_clientes),
    path("listar_servicios", listar_servicios),
    path("usuario/token/<str:token>", obtener_usuario_token),
    path("registrar/usuario/", registrar_usuario.as_view()),
    path("duenyo_recintos/<int:duenyo_id>/recintos/", recintos_by_duenyo),
    path("recinto/post/", recinto_create),
]
