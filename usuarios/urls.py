from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import ( TokenObtainPairView,TokenRefreshView,)
from .views import UserRegisterView, UploadCVView, LoginView, CategoriaServicioView, AvailableServicesView,SendNotificationView,UpdateNotificationView,ServiceListView,CreateServiceView,SolicitudViewSet
router = DefaultRouter()
router.register(r'solicitudes', SolicitudViewSet)

urlpatterns = [
    path('servis_api/usuarios/', include(router.urls)),  # Incluye las rutas generadas por el router
    path('register/', UserRegisterView.as_view(), name='register'),
    path('upload_cv/', UploadCVView.as_view(), name='upload_cv'),
    path('login/', LoginView.as_view(), name='login'),
    # Rutas de autenticación con JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     # Servicios disponibles
    path('services/', AvailableServicesView.as_view(), name='available_services'),
    path('categorias/', CategoriaServicioView.as_view(), name='categorias'),
    # Notificaciones
    path('notifications/send/', SendNotificationView.as_view(), name='send_notification'),
    path('notifications/<int:pk>/update/', UpdateNotificationView.as_view(), name='update_notification'),

    path('servicios/', ServiceListView.as_view(), name='service-list'),
    path('crear-servicio/', CreateServiceView.as_view(), name='create-service'),
]