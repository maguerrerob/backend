from django.contrib import admin
from .models import *

# Register your models here.

misModelos = [
    Cliente,
    Servicio,
    RecintoServicio,
    Duenyo_recinto,
    Recinto
]

admin.site.register(misModelos)