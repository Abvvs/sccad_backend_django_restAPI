from django.db import models
from .catalogos import EstadoTrabajo, TipoTrabajo
from django.contrib.auth.models import User


class Trabajo(models.Model):
    ESTADO_PAGO = [
        ('PENDIENTE', 'Pendiente'),
        ('PARCIAL', 'Parcial'),
        ('PAGADO', 'Pagado'),
        ('CANCELADO', 'Trabajo Cancelado (no se culminó)'),
    ]

    PRIORIDAD = [
        ('BAJA', 'Baja'),
        ('NORMAL', 'Normal'),
        ('ALTA', 'Alta'),
        ('URGENTE', 'Urgente'),
    ]

    numero_trabajo = models.CharField(max_length=50, unique=True)
    tipo_trabajo = models.ForeignKey(TipoTrabajo, on_delete=models.PROTECT, related_name='trabajos')
    #cliente = models.ForeignKey(Persona, on_delete=models.PROTECT, related_name='trabajos')
    descripcion = models.TextField()
    direccion_campo = models.TextField(blank=True, null=True)
    referencia_ubicacion = models.TextField(blank=True, null=True)
    monto_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    saldo_pendiente = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado_pago = models.CharField(max_length=20, choices=ESTADO_PAGO, default='PENDIENTE')
    estado_trabajo_actual = models.ForeignKey(
        EstadoTrabajo,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='trabajos_actuales'
    )
    prioridad = models.CharField(max_length=20, choices=PRIORIDAD, default='NORMAL')
    observaciones = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Trabajo"
        verbose_name_plural = "Trabajos"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.numero_trabajo} - {self.descripcion[:40]}"


class TrabajoEstadoHistorial(models.Model):
    trabajo = models.ForeignKey(Trabajo, on_delete=models.CASCADE, related_name='historial_estados')
    estado_trabajo = models.ForeignKey(EstadoTrabajo, on_delete=models.PROTECT)
    fecha_cambio = models.DateTimeField(auto_now_add=True)
    usuario_responsable = models.CharField(max_length=100, blank=True, null=True)
    departamento_actual = models.CharField(max_length=100, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    documentos_requeridos = models.TextField(blank=True, null=True)
    fecha_estimada_siguiente_paso = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Historial de estado"
        verbose_name_plural = "Historial de estados"
        ordering = ['-fecha_cambio']

    def __str__(self):
        return f"{self.trabajo.numero_trabajo} → {self.estado_trabajo.nombre}"

class TrabajoPersona(models.Model):
    trabajo = models.ForeignKey(
        "trabajos.Trabajo",
        on_delete=models.CASCADE,
        related_name="personas_relacionadas"
    )
    """ persona = models.ForeignKey(
        "personas.Persona",  # asegúrate de tener la app personas o ajusta el nombre
        on_delete=models.CASCADE,
        related_name="trabajos_relacionados"
    ) """
    """ tipo_etiqueta = models.ForeignKey(
        "trabajos.TipoEtiquetaPersona",  # o donde tengas el catálogo de etiquetas
        on_delete=models.CASCADE
    ) """
    #es_contacto_principal = models.BooleanField(default=False)
    #orden_visualizacion = models.PositiveIntegerField(default=0)
    observaciones = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        #unique_together = ('trabajo', 'persona', 'tipo_etiqueta')
        verbose_name = "Relación Trabajo-Persona"
        verbose_name_plural = "Relaciones Trabajo-Persona"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.trabajo}"