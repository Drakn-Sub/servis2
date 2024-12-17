from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Usuarios, Trabajador, Cliente, Service, CategoriaServicio,Notification,Solicitud
from .serializers import UserSerializer, TrabajadorSerializer, ClienteSerializer, CategoriaServicioSerializer , ServiceSerializer, NotificationSerializer,SolicitudSerializer

import random

# Vista para registro de usuario
class UserRegisterView(generics.CreateAPIView):
    queryset = Usuarios.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        telefono = request.data.get('telefono')
        tipo_usuario = request.data.get('tipo_usuario')
        password = request.data.get('password')
        
        if tipo_usuario not in ['cliente', 'trabajador']:
            return Response({"error": "Tipo de usuario inválido"}, status=status.HTTP_400_BAD_REQUEST)
 # Verificar si el usuario ya existe por email o RUT
        email = request.data.get('email')
        rut = request.data.get('rut')
        
        if Usuarios.objects.filter(email=email).exists():
            return Response({"error": "El correo ya está registrado."}, status=status.HTTP_400_BAD_REQUEST)
        
        if Usuarios.objects.filter(rut=rut).exists():
            return Response({"error": "El RUT ya está registrado."}, status=status.HTTP_400_BAD_REQUEST)

        # Crear el usuario
        user_data = {
            'telefono': telefono,
            'tipo_usuario': tipo_usuario,
            'nombre': request.data.get('nombre'),
            'email': request.data.get('email'),
            'rut': request.data.get('rut'),
            'password': make_password(password)  # Encriptar la contraseña
        }

       
        serializer = self.get_serializer(data=user_data)

        if serializer.is_valid():
            user = serializer.save()
            if tipo_usuario == 'trabajador':
                trabajador, created = Trabajador.objects.get_or_create(user=user) 
            elif tipo_usuario == 'cliente':
                cliente, created = Cliente.objects.get_or_create(user=user)
            """
            if tipo_usuario == 'trabajador':
                Trabajador.objects.create(user=user)  # Crear perfil trabajador
            elif tipo_usuario == 'cliente':
                Cliente.objects.create(user=user)  # Crear perfil cliente
            """
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vista login 2
class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        rut = request.data.get('rut')
        password = request.data.get('password')
        user = Usuarios.objects.filter(rut=rut).first()

        if not user:
            return Response({"error": "El RUT no existe"}, status=400)

        if not check_password(password, user.password):
            return Response({"error": "Contraseña incorrecta"}, status=400)

        # Generar el token de acceso si las credenciales son correctas
        refresh = RefreshToken.for_user(user)

        # Retornar el token junto con el tipo de usuario
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'tipo_usuario': user.tipo_usuario  # Aquí incluimos el tipo de usuario
        }, status=status.HTTP_200_OK)

# Subir archivos solo para Trabajadores
class UploadCVView(generics.UpdateAPIView):
    queryset = Trabajador.objects.all()
    serializer_class = TrabajadorSerializer
 

    def put(self, request, pk=None):
        user = request.user
        if user.tipo_usuario != 'trabajador':
            return Response({"error": "Solo trabajadores pueden subir archivos"}, status=status.HTTP_403_FORBIDDEN)
        
        trabajador = Trabajador.objects.get(user=user)
        serializer = self.serializer_class(trabajador, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Archivo subido exitosamente"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Categoria service
class CategoriaServicioView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        categorias = CategoriaServicio.objects.all()
        serializer = CategoriaServicioSerializer(categorias, many=True)
        return Response(serializer.data)

class ServiceListView(APIView):
    def get(self, request):
        tipo_servicio = request.query_params.get('tipo_servicio', None)
        ubicacion = request.query_params.get('ubicacion', None)  # Si implementas geolocalización en el futuro
        servicios = Service.objects.all()
        
        if tipo_servicio:
            servicios = servicios.filter(categoria__nombre=tipo_servicio)
        
        if ubicacion:
            # Este filtro dependerá de cómo implementes la geolocalización en tu modelo
            servicios = servicios.filter(ubicacion__icontains=ubicacion)
        
        serializer = ServiceSerializer(servicios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateServiceView(APIView):
    def post(self, request):
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(trabajador=request.user)  # Asociar el trabajador logueado
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
class AvailableServicesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categoria = request.query_params.get('categoria', None)
        servicios = Service.objects.all()
        if categoria:
            servicios = servicios.filter(categoria__nombre=categoria)
        serializer = ServiceSerializer(servicios, many=True)
        return Response(serializer.data)

class SendNotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cliente_id = request.data.get('cliente_id')
        trabajador_id = request.data.get('trabajador_id')
        mensaje = "Le ha llegado una solicitud de trabajo."
        notification = Notification.objects.create(
            trabajador_id=trabajador_id,
            cliente_id=cliente_id,
            mensaje=mensaje
        )
        return Response({'detail': 'Solicitud enviada correctamente.', 'notification_id': notification.id})

class SolicitudViewSet(viewsets.ModelViewSet):
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer

    def perform_create(self, serializer):
        serializer.save(cliente=self.request.user)

class UpdateNotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        estado = request.data.get('estado')
        notification = Notification.objects.get(id=pk)
        notification.estado = estado
        notification.save()
        return Response({'detail': f'Notificación actualizada a {estado}.'})
