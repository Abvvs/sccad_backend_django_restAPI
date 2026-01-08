from django.db import models
from django.utils import timezone
from cuenta_cobrar.models import CuentaCobrar
from trabajos.models.catalogos import FormaPago 


class Pago(models.Model):
    cuenta_cobrar = models.ForeignKey(
        CuentaCobrar,
        on_delete=models.PROTECT,
        related_name="pagos"
    )
    forma_pago = models.ForeignKey(FormaPago, on_delete=models.PROTECT)
    fecha_pago = models.DateTimeField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    observaciones = models.TextField(null=True, blank=True)
    recibido_por = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recibo {self.cuenta_cobrar} - ${self.monto}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.monto <= 0:
            raise ValidationError("El monto del pago debe ser mayor a 0")

        if self.monto > self.cuenta_cobrar.saldo_pendiente:
            raise ValidationError("El pago no puede exceder el saldo pendiente")
