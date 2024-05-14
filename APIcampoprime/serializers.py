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