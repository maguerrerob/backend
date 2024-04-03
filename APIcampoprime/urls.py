from django.urls import path
from  .views import *

urlpatterns = [
    path("listar_clientes", listar_clientes)
]
