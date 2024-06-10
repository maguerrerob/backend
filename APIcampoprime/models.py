from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.

class Usuario(AbstractUser):
    ADMINISTRADOR = 1
    CLIENTE = 2
    DUENYO_RECINTO = 3
    ROLES = (
        (ADMINISTRADOR, "administrador"),
        (CLIENTE, "cliente"),
        (DUENYO_RECINTO, "duenyo_recinto")
    )
    rol = models.PositiveSmallIntegerField(
        choices=ROLES, default=1
    )
    
    def __str__(self):
        return self.username
    
class Cliente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=9)

    def __str__(self) -> str:
        return self.usuario.username

class Duenyo_recinto(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=9)

    def __str__(self) -> str:
        return self.usuario.username

class Recinto(models.Model):
    duenyo_recinto = models.ForeignKey(Duenyo_recinto, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    ciudad = models.CharField(max_length=50)
    precio_por_hora = models.FloatField()
    imagen = models.ImageField(upload_to='recintos', blank=True, null=True)
    hora_inicio = models.FloatField()
    hora_fin = models.FloatField()

    def __str__(self) -> str:
        return self.nombre
    
class Pista(models.Model):
    recinto = models.ForeignKey(Recinto, verbose_name=("Recinto"), on_delete=models.CASCADE)
    ESTADOS = [
        ("B", "Bueno"),
        ("M", "Mal"),
        ("R", "Regular")
    ]
    estado_porterias = models.CharField(max_length=1, choices=ESTADOS)
    n_pista = models.IntegerField()
    CAMPOS = [
        ("SA", "Sala"),
        ("SI", "Siete"),
        ("ON", "Once")
    ]
    tipo_campo = models.CharField(max_length=2, choices=CAMPOS)

class Reserva(models.Model):
    cliente = models.ForeignKey(Cliente, verbose_name=("Cliente"), on_delete=models.CASCADE)
    pista = models.ForeignKey(Pista, verbose_name=("Pista"), on_delete=models.CASCADE)
    hora_inicio = models.FloatField()
    hora_fin = models.FloatField()
    dia = models.DateField(default=timezone.now)

class Servicio(models.Model):
    recinto = models.ForeignKey(Recinto, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    observaciones = models.TextField()

    def __str__(self) -> str:
        return self.nombre