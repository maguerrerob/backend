from django.contrib import admin
from .models import *

# Register your models here.

misModelos = [
    Cliente
]

admin.site.register(misModelos)