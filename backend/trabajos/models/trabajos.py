from django.db import models
from .catalogos import EstadoTrabajo, TipoTrabajo
from django.contrib.auth.models import User
from clientes.models import Cliente


class Trabajo(models.Model):
    ESTADO_PAGO = [
        ('PENDIENTE', 'Pendiente'),
        ('PARCIAL', 'Parcial'),
        ('PAGADO', 'Pagado'),
        ('CANCELADO', 'Trabajo Cancelado (no se culminó)'),
    ]


    numero_trabajo = models.CharField(max_length=50, unique=True)
    tipo_trabajo = models.ForeignKey(TipoTrabajo, on_delete=models.PROTECT, related_name='trabajos')
    cliente = models.ManyToManyField(Cliente, through='TrabajoCliente', related_name='trabajos')
    descripcion = models.TextField()
    direccion_campo = models.TextField(blank=True, null=True)
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
    estado_trabajo = models.ForeignKey(EstadoTrabajo, on_delete=models.PROTECT, null= True)
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

class TrabajoCliente(models.Model):
    TIPO_ETIQUETA_CLIENTE_CHOICES = [
        ('PRINCIPAL', 'Principal'),
        ('PROPIETARIO', 'Propietario'),
        ('CONTACTO', 'Contacto'),
    ]
    trabajo = models.ForeignKey(
        Trabajo,
        on_delete=models.CASCADE,
        related_name="clientes_relacionadas"
    )
    cliente = models.ForeignKey(
        Cliente,  # asegúrate de tener la app personas o ajusta el nombre
        on_delete=models.CASCADE,
        related_name="trabajos_relacionados"
    )
    tipo_etiqueta = models.CharField(
        max_length=20,
        choices=TIPO_ETIQUETA_CLIENTE_CHOICES,
    )
    observaciones = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('trabajo', 'cliente', 'tipo_etiqueta')
        verbose_name = "Relación Trabajo-Persona"
        verbose_name_plural = "Relaciones Trabajo-Persona"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.trabajo.numero_trabajo} - {self.cliente.nombre} ({self.tipo_etiqueta})"