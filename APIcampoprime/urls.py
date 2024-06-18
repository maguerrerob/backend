from django.urls import path
from  .views import *

urlpatterns = [
    path("listar_clientes", listar_clientes),
    path("listar_servicios", listar_servicios),
    path("usuario/token/<str:token>", obtener_usuario_token),
    path("registrar/usuario/", registrar_usuario.as_view()),
    path("duenyo_recintos/<int:duenyo_id>/recintos/", recintos_by_duenyo),
    path("getDuenyorecintoId/<int:usuario_id>", get_duenyo_recinto_id),
    path("recinto/post/", recinto_create),
    path("recinto/lista", obtener_recintos),
    path("getReservas/recinto/<int:id_recinto/", getReservas),
    path("crear_reserva", crear_reserva),
    path("horario/recinto/<int:idRecinto>", getHorarioRecinto),
    path("reservas/<int:recinto_id>/<str:dia>/", obtener_reservas)
]
