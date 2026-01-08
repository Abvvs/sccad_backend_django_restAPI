from django.db import models
from trabajos.models.catalogos import FormaPago
from pago.models import Pago 

class MovimientoCaja(models.Model):
    TIPO_MOVIMIENTO = [
        ('INGRESO', 'Ingreso'),
        ('EGRESO', 'Egreso'),
    ]
    pago = models.ForeignKey(
        Pago,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="movimientos_caja"
    )
    tipo_movimiento = models.CharField(max_length=20, choices=TIPO_MOVIMIENTO)
    forma_pago = models.ForeignKey(FormaPago, on_delete=models.PROTECT)
    fecha_movimiento = models.DateField(auto_now_add=True)

    monto = models.DecimalField(max_digits=10, decimal_places=2)
    concepto = models.TextField()
    responsable = models.CharField(max_length=100, null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo_movimiento} - {self.monto} - {self.fecha_movimiento}"
