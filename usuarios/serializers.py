from rest_framework import serializers
from .models import Usuarios,Trabajador,Cliente, Service, CategoriaServicio, Notification, Solicitud

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        #fields = ['id', 'rut', 'name', 'email', 'phone_number']
        #fields = ['id', 'rut', 'name', 'email', 'phone_number', 'tipo_usuario', 'verified']
        #fields = '__all__'
        fields = ['telefono', 'tipo_usuario', 'nombre', 'email', 'rut','password']  
    
    """Crear usuario sin verificacion de tipo
    def create(self, validated_data):
        user = Usuarios(**validated_data)
        user.save()
        return user
    """
    def create(self, validated_data):
        user = Usuarios.objects.create(**validated_data)
        tipo_usuario = validated_data.get('tipo_usuario')
        
        # Crear perfil de Trabajador o Cliente
        if tipo_usuario == 'trabajador':
            Trabajador.objects.get_or_create(user=user)
        elif tipo_usuario == 'cliente':
            Cliente.objects.get_or_create(user=user)
        
        return user

class TrabajadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trabajador
        #fields = ['archivo_cv']
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        #fields =[]
        fields = '__all__'

class CategoriaServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaServicio
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    trabajador_nombre = serializers.CharField(source='trabajador.nombre', read_only=True)
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)

    class Meta:
        model = Service
        fields = [
            'id', 'titulo', 'descripcion', 'categoria', 'categoria_nombre', 'trabajador', 'trabajador_nombre',
            'precio', 'calificacion', 'horarios_disponibles', 'contacto', 'cliente_solicitante', 'creado_en'
        ]

class NotificationSerializer(serializers.ModelSerializer):
    trabajador_nombre = serializers.CharField(source='trabajador.user.nombre', read_only=True)
    cliente_nombre = serializers.CharField(source='cliente.user.nombre', read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'trabajador', 'trabajador_nombre', 'cliente', 'cliente_nombre', 'mensaje', 'estado', 'creado_en']

class SolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = ['cliente', 'trabajador', 'servicio', 'mensaje', 'estado']
