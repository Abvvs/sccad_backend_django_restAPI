from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Sum
from decimal import Decimal

class TipoServicio(models.Model):
    CATEGORIAS = [
        ('IMPRESION', 'Impresión'),
        ('VENTA', 'Venta'),
        ('COPIA', 'Copia'),
        ('OTRO', 'Otro'),
    ]
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    unidad_medida = models.CharField(max_length=20, default="unidad")
    estado = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Tipo de servicio"
        verbose_name_plural = "Tipos de servicio"

    def __str__(self):
        return f"{self.nombre} ({self.categoria})"

class ServicioAdicional(models.Model):
    """Servicios adicionales (impresiones, copias, ventas)"""
    
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('PAGADO', 'Pagado'),
        ('CANCELADO', 'Cancelado'),
    ]

    numero_servicio = models.CharField(max_length=50, unique=True)
    cliente = models.ForeignKey(
        'clientes.Cliente', 
        on_delete=models.PROTECT,
        related_name='servicios_adicionales',
        null=True,
        blank=True
    )
    fecha_servicio = models.DateField(auto_now_add=True)
    descripcion = models.TextField(blank=True, null=True)
    monto_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0'))]
    )
    saldo_pendiente = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0'))]
    )
    estado_pago = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='PENDIENTE'
    )
    observaciones = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'servicio_adicional'
        verbose_name = 'Servicio Adicional'
        verbose_name_plural = 'Servicios Adicionales'
        ordering = ['-fecha_servicio', '-id']

    def __str__(self):
        return f"{self.numero_servicio} - {self.cliente}"

    def calcular_totales(self):
        """Calcula el monto total basado en los detalles"""
        total = self.detalles.aggregate(
            total=Sum('subtotal')
        )['total'] or Decimal('0.00')
        
        self.monto_total = total
        if self.saldo_pendiente > self.monto_total:
            self.saldo_pendiente = self.monto_total
        self.save(update_fields=['monto_total', 'saldo_pendiente', 'updated_at'])
        return total

    def actualizar_estado_pago(self):
        """Actualiza el estado según el saldo pendiente"""
        if self.saldo_pendiente == 0:
            self.estado_pago = 'PAGADO'
        elif self.saldo_pendiente < self.monto_total:
            self.estado_pago = 'PARCIAL'
        else:
            self.estado_pago = 'PENDIENTE'
        self.save(update_fields=['estado_pago', 'updated_at'])

    def save(self, *args, **kwargs):
        # Generar número de servicio automático si no existe
        if not self.numero_servicio:
            from datetime import datetime
            year = datetime.now().year
            last_service = ServicioAdicional.objects.filter(
                numero_servicio__startswith=f'SRV-{year}'
            ).order_by('-id').first()
            
            if last_service:
                last_num = int(last_service.numero_servicio.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            
            self.numero_servicio = f'SRV-{year}-{new_num:04d}'
        
        super().save(*args, **kwargs)


class ServicioAdicionalDetalle(models.Model):
    """Detalle de servicios adicionales"""
    
    servicio_adicional = models.ForeignKey(
        ServicioAdicional,
        on_delete=models.CASCADE,
        related_name='detalles'
    )
    tipo_servicio = models.ForeignKey(
        TipoServicio,
        on_delete=models.PROTECT,
        related_name='detalles_servicio'
    )
    cantidad = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('1.00'),
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0'))]
    )
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'servicio_adicional_detalle'
        verbose_name = 'Detalle de Servicio'
        verbose_name_plural = 'Detalles de Servicios'
        ordering = ['id']

    def __str__(self):
        return f"{self.tipo_servicio.nombre} x {self.cantidad}"

    def save(self, *args, **kwargs):
        # Calcular subtotal automáticamente
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
        
        # Actualizar totales del servicio padre
        self.servicio_adicional.calcular_totales()