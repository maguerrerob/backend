from datetime import datetime
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
from rest_framework.views import APIView
from django.db.models import Q


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
        print(request.data)
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
                    if not Group.objects.filter(name='cliente').exists():
                        Group.objects.create(name='cliente')
                    grupo = Group.objects.get(name='cliente')
                    grupo.user_set.add(user)
                    telefono = serializers.validated_data.get('telefono')
                    cliente = Cliente.objects.create(usuario=user, telefono=telefono)
                    cliente.save()
                elif (rol == str(Usuario.DUENYO_RECINTO)):
                    if not Group.objects.filter(name='duenyo_recinto').exists():
                        Group.objects.create(name='duenyo_recinto')
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
            print(repr(serializers.errors))
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(["GET"])
def recintos_by_duenyo(request, duenyo_id):
    print(request.data)
    existe = Recinto.objects.filter(duenyo_recinto=duenyo_id).exists()
    return Response(existe)

@api_view(['GET'])
def get_duenyo_recinto_id(request, usuario_id):
    try:
        # Obtener el objeto Usuario
        usuario = Usuario.objects.get(id=usuario_id)
        
        # Obtener el objeto Duenyo_recinto correspondiente al usuario
        duenyo_recinto = Duenyo_recinto.objects.get(usuario=usuario)
        
        # Devolver el ID de Duenyo_recinto
        return Response({"duenyo_recinto_id": duenyo_recinto.id}, status=status.HTTP_200_OK)
    
    except Usuario.DoesNotExist:
        return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
    except Duenyo_recinto.DoesNotExist:
        return Response({"error": "Duenyo_recinto no encontrado para el usuario dado"}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def recinto_create(request):
    print(request.data)
    serializer = RecintoSerializerCreate(data=request.data)
    if serializer.is_valid():
        try:
            recinto = serializer.save()
            return Response({"id": recinto.id,
                                "nombre": recinto.nombre,
                                "descripcion": recinto.descripcion,
                                "ciudad": recinto.ciudad,
                                "precio_por_hora": recinto.precio_por_hora,
                                "hora_inicio": recinto.hora_inicio,
                                "hora_fin": recinto.hora_fin,
                            }, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as error:
            print(repr(error))
            return Response(str(error), status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print(repr(error))
            return Response(str(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getReservas(request, id_recinto):
    try:
        # Filtrar las reservas para el recinto dado
        reservas = Reserva.objects.filter(recinto_id=id_recinto)
        
        # Si no hay reservas, lanzar una excepción personalizada
        if not reservas.exists():
            raise Reserva.DoesNotExist

        # Convertir las reservas a una lista de diccionarios
        lista_reservas = list(reservas.values('cliente__nombre', 'hora_inicio', 'hora_fin', 'dia'))
        return Response({"Reservas": lista_reservas}, status=status.HTTP_200_OK)
    
    except Reserva.DoesNotExist:
        return Response({"error": "No se encontraron reservas para el recinto especificado."}, status=status.HTTP_404_NOT_FOUND)
    
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({"error": "Error interno del servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def obtener_recintos(request):
    recintos = Recinto.objects.all()
    serializer = RecintoSerializer(recintos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def getHorarioRecinto(request, idRecinto):
    try:
        recinto = Recinto.objects.get(id=idRecinto)
        return Response({"hora_inicio": recinto.hora_inicio, "hora_fin": recinto.hora_fin}, status=status.HTTP_200_OK)
    
    except Reserva.DoesNotExist:
        return Response({"error": "Reserva no encontrada."}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        print(repr(e))
        return Response({"error": "Error interno del servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["GET"])
def obtener_reservas(request, recinto_id, dia):
    try:
        # Convertir el día de string a objeto date
        dia = datetime.strptime(dia, '%Y-%m-%d').date()
        reservas = Reserva.objects.filter(recinto_id=recinto_id, dia=dia)
        
        # Crear un diccionario para marcar las horas reservadas
        horas_reservadas = {}
        for reserva in reservas:
            for hora in range(int(reserva.hora_inicio), int(reserva.hora_fin)):
                horas_reservadas[hora] = True

        return Response(horas_reservadas)
    except Exception as e:
        print(repr(e))
        return Response({'error': str(e)}, status=500)
    
@api_view(['GET'])
def buscar_recintos(request):
    query = request.query_params.get('query', '')

    recintos = Recinto.objects.filter(
        Q(nombre__icontains=query) | Q(ciudad__icontains=query)
    )

    serializer = RecintoSerializer(recintos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def obtenerRecinto(request, idRecinto):
    try:
        recinto = Recinto.objects.get(id=idRecinto)
    except Recinto.DoesNotExist:
        return Response("Recinto no encontrado")
    
    serializer = RecintoSerializer(recinto)
    return Response(serializer.data)

@api_view(['POST'])
def crear_reserva(request):
    print(request.data)
    serializer = ReservaSerializerCreate(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response("Reserva creada")
        except serializers.ValidationError as error:
            print(repr(error))
            return Response(str(error), status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print(repr(error))
            return Response(str(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def obtener_cliente(request, usuario_id):
    try:
        cliente = Cliente.objects.get(usuario=usuario_id)
        serializer = ClienteSerializer(cliente)
        return Response(serializer.data)
    except Exception as error:
        print(repr(error))
        return Response(str(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)