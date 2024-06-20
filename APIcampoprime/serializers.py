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
    
class RecintoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recinto
        fields = [
            'id', 'nombre', 
            'descripcion', 'ciudad', 
            'precio_por_hora', 'hora_inicio', 
            'hora_fin'
        ]

class ReservaSerializer(serializers.Serializer):
    class Meta:
        model = Reserva
        fiels = "__all__"

class DuenyoRecintoSerializer(serializers.ModelSerializer):
    recintos = RecintoSerializer(many=True, read_only=True)

    class Meta:
        model = Duenyo_recinto
        fields = "__all__"

class RecintoSerializerCreate(serializers.ModelSerializer):
    duenyo_recinto = serializers.PrimaryKeyRelatedField(queryset=Duenyo_recinto.objects.all())
    class Meta:
        model = Recinto
        fields = ["duenyo_recinto","descripcion", "nombre",
            "ciudad", "precio_por_hora",
            "hora_inicio", "hora_fin"
        ]
    
    def validate_descripcion(self, descripcion):
        if len(descripcion) > 500:
            raise serializers.ValidationError("Error, no puede tener una descripción tan larga")
        return descripcion

    # def validate_nombre(self, nombre):
    #     QSnombre = Recinto.objects.filter(nombre=nombre).first()
    #     if (QSnombre is not None):
    #         raise serializers.ValidationError("Error, ese nombre de recinto ya existe")
    #     return nombre

    

    # def validate_precio_por_hora(self, precio_por_hora):
    #     if precio_por_hora < 6:
    #         raise serializers.ValidationError("Error, el precio no puede ser menor de 1")
    #     return precio_por_hora

class ReservaSerializerCreate(serializers.ModelSerializer):
    cliente = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all())
    recinto = serializers.PrimaryKeyRelatedField(queryset=Recinto.objects.all())

    class Meta:
        model = Reserva
        fields = [
            'cliente', 'recinto',
            'hora_inicio', 'hora_fin',
            'dia'
        ]

    # def validate_hora_inicio(self, hora_inicio):
    #     data = self.get_initial()
    #     hora_fin = data.get('hora_fin')
    #     if hora_inicio > hora_fin:
    #         raise serializers.ValidationError("Error, la hora de fin")
    #     return hora_inicio
