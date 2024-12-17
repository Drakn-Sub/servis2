from django.db import models
from django.contrib.auth.hashers import make_password

class Usuarios(models.Model):
    TIPO_USUARIO_CHOICES = [
        ('cliente', 'Cliente'),
        ('trabajador', 'Trabajador'),
    ]
    rut = models.CharField(max_length=12, unique=True)  # Campo RUT, único
    nombre = models.CharField(max_length=100)  # Campo nombre completo
    email = models.EmailField(unique=True)  # Campo email, único
    telefono = models.CharField(max_length=15, unique=True)  # Campo teléfono, único
    tipo_usuario = models.CharField(max_length=10, choices=TIPO_USUARIO_CHOICES,default='cliente')
    password = models.CharField(max_length=128, default='temporary_password')  # Campo para la contraseña (encriptada)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Encriptar la contraseña antes de guardarla en la base de datos
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        #return f"{self.name} - {self.email}"
        return f"{self.nombre} ({self.tipo_usuario}) - {self.email}"
        
class Trabajador(models.Model):
    user = models.OneToOneField(Usuarios, on_delete=models.CASCADE, primary_key=True)
    archivo_cv = models.FileField(upload_to='upload_cv/', blank=True, null=True)  # PDF/Word

    def __str__(self):
        return f"Trabajador: {self.user.nombre} -Telefono: {self.user.telefono}"

class Cliente(models.Model):
    user = models.OneToOneField(Usuarios, on_delete=models.CASCADE, primary_key=True)
    
    def __str__(self):
        return f"Cliente: {self.user.nombre} - Telefono: {self.user.telefono}"

class CategoriaServicio(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Service(models.Model):
    titulo = models.CharField(max_length=150, default='sin titulo')
    descripcion = models.TextField()
    categoria = models.ForeignKey(CategoriaServicio, on_delete=models.CASCADE)
    trabajador = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='service', null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Nuevo
    calificacion = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)  # Nuevo
    horarios_disponibles = models.CharField(max_length=255, default="9:00 AM - 5:00 PM")  # Nuevo
    contacto = models.CharField(max_length=50, default="N/A")  # Nuevo
    cliente_solicitante = models.ForeignKey(
        Usuarios, on_delete=models.SET_NULL, related_name='solicitudes', null=True, blank=True
    )  # Relación con cliente
    creado_en = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.titulo} - {self.trabajador.nombre}"

class Notification(models.Model):
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE, related_name='notifications')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='notifications')
    mensaje = models.CharField(max_length=255)
    estado = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('aceptada', 'Aceptada'), ('rechazada', 'Rechazada')], default='pendiente')
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notificación para {self.trabajador.user.nombre} - {self.estado}"

class Solicitud(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="solicitudes_cliente")
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE,related_name="solicitudes_trabajador")
    servicio = models.ForeignKey(Service, on_delete=models.CASCADE)
    mensaje = models.TextField()
    estado = models.CharField(max_length=10, choices=[('Pendiente', 'Pendiente'), ('Aceptado', 'Aceptado'), ('Rechazado', 'Rechazado')])