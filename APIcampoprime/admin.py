from django.contrib import admin
from .models import *

# Register your models here.

misModelos = [
    Cliente,
    Servicio,
    Pista,
    Duenyo_recinto,
    Recinto,
    Reserva,
]

admin.site.register(misModelos)