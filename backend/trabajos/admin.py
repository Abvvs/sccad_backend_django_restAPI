from django.contrib import admin
from .models import *
admin.site.register(EstadoTrabajo)
admin.site.register(TipoTrabajo)
admin.site.register(FormaPago)
admin.site.register(Trabajo)
admin.site.register(TrabajoEstadoHistorial)
admin.site.register(TrabajoCliente)

# Register your models here.
