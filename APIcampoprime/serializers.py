from rest_framework import serializers
from .models import *

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = "__all__"

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = "__all__"

class UsuarioSerializerRegistro(serializers.Serializer):
    username = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    telefono = serializers.CharField(max_length=9)
    rol = serializers.IntegerField()

    def validate_username(self, username):
        usuario = Usuario.objects.filter(username=username).first()
        if (not usuario is None):
            raise serializers.ValidationError("Ya existe un usuario con ese nombre")
        return username
    
    def validate_password1(self, password1):
        data = self.get_initial()
        password2 = data.get('password2')
        if password1 != password2:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        return password1
    
class RecintoSerializer(serializers.Serializer):
    class Meta:
        model = Recinto
        fields = "__all__"

class DuenyoRecintoSerializer(serializers.ModelSerializer):
    recintos = RecintoSerializer(many=True, read_only=True)

    class Meta:
        model = Duenyo_recinto
        fields = "__all__"

class RecintoSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Recinto
        fields = "__all__"

    # def validate_nombre(self, nombre):
    #     QSnombre = Recinto.objects.filter(nombre=nombre).first()
    #     if (QSnombre is not None):
    #         raise serializers.ValidationError("Error, ese nombre de recinto ya existe")
    #     return nombre

    def validate_descripcion(self, descripcion):
        if len(descripcion) > 500:
            raise serializers.ValidationError("Error, no puede tener una descripción tan larga")
        return descripcion

    # def validate_precio_por_hora(self, precio_por_hora):
    #     if precio_por_hora < 6:
    #         raise serializers.ValidationError("Error, el precio no puede ser menor de 1")
    #     return precio_por_hora