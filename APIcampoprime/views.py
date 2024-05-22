from django.shortcuts import render
from .models import Cliente
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from oauth2_provider.models import AccessToken
# Para registro
from rest_framework import generics
# Para permitir todo el acceso a la vista
from rest_framework.permissions import AllowAny
# Para usar grupos de Django
from django.contrib.auth.models import Group
# Para indicar errores (500, 400, 401, etc)
from rest_framework import status


# Create your views here.

@api_view(["GET"])
def listar_clientes(request):
    clientes = Cliente.objects.all()
    serializer = ClienteSerializer(clientes, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def listar_servicios(request):
    servicios = Servicio.objects.all()
    serializer = ServicioSerializer(servicios, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def obtener_usuario_token(request, token):
    try:
        access_token_obj = AccessToken.objects.get(token=token)
        user = access_token_obj.user
        serializer = UsuarioSerializer(user)
        return Response(serializer.data)
    except AccessToken.DoesNotExist:
        return None
    
class registrar_usuario(generics.CreateAPIView):
    serializer_class = UsuarioSerializerRegistro
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializers = UsuarioSerializerRegistro(data=request.data)
        if serializers.is_valid():
            try:
                rol = request.data.get('rol')
                user = Usuario.objects.create_user(
                    username = serializers.data.get('username'),
                    email = serializers.data.get('email'),
                    password = serializers.data.get('password1'),
                    first_name = serializers.data.get('first_name'),
                    last_name = serializers.data.get('last_name'),
                    rol = rol
                )
                if (rol == str(Usuario.CLIENTE)):
                    grupo = Group.objects.get(name='cliente')
                    grupo.user_set.add(user)
                    telefono = serializers.validated_data.get('telefono')
                    cliente = Cliente.objects.create(usuario=user, telefono=telefono)
                    cliente.save()
                elif (rol == str(Usuario.DUENYO_RECINTO)):
                    grupo = Group.objects.get(name='duenyo_recinto')
                    grupo.user_set.add(user)
                    telefono = serializers.validated_data.get('telefono')
                    duenyo_recinto = Duenyo_recinto.objects.create(usuario=user, telefono=telefono)
                    duenyo_recinto.save()
                usuarioSerializado = UsuarioSerializer(user)
                return Response(usuarioSerializado.data)
            except Exception as error:
                print(repr(error))
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)