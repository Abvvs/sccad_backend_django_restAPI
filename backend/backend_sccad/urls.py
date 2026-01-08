from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('trabajos/', include('trabajos.urls')),
    path('empleados/', include('empleados.urls')),
    path('clientes/', include('clientes.urls')),
    path('servicio-adicional/', include('servicio_adicional.urls')),
    path('cuenta_cobrar/', include('cuenta_cobrar.urls')),
    path('pago/', include('pago.urls')),
    path('movimiento_caja/', include('movimiento_caja.urls'))
]
