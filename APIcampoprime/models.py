from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

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
    id_duenyo_recinto = models.ForeignKey(Duenyo_recinto, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    ciudad = models.CharField(max_length=50)
    municipio = models.CharField(max_length=50)
    precio_por_hora = models.IntegerField()

    def __str__(self) -> str:
        return self.nombre

class Servicio(models.Model):
    servicio_ofrecido = models.ManyToManyField(Recinto, through="RecintoServicio")
    nombre = models.CharField(max_length=50)
    observaciones = models.TextField()

    def __str__(self) -> str:
        return self.nombre

class RecintoServicio(models.Model):
    recinto = models.ForeignKey(Recinto, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.id

    class Meta:
        unique_together = ('recinto', 'servicio')  # Asegura que no haya duplicados para que un Servicio no pueda ser servido más de una vez en el Recinto