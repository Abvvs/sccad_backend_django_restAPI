from django.db import models
from django.db.models import Sum
from decimal import Decimal
from django.forms import ValidationError
from trabajos.models import Trabajo
from servicio_adicional.models import ServicioAdicional

class CuentaCobrar(models.Model):
    TIPO_CUENTA_CHOICES = [
        ("TRABAJO", "Trabajo"),
        ("SERVICIO", "Servicio adicional"),
    ]

    ESTADO_CHOICES = [
        ("PENDIENTE", "Pendiente"),
        ("PARCIAL", "Parcial"),
        ("PAGADO", "Pagado"),
        ("VENCIDO", "Vencido"),
        ("CANCELADO", "Cancelado"),
    ]
    numero_cuenta = models.CharField(max_length=50, unique=True)
    cliente = models.ForeignKey('clientes.Cliente', on_delete=models.PROTECT, related_name="cuentas")
    trabajo = models.OneToOneField(
        Trabajo, on_delete=models.PROTECT, null=True, blank=True, related_name="cuenta"
    )
    servicio_adicional = models.ForeignKey(
        ServicioAdicional, on_delete=models.PROTECT, null=True, blank=True, related_name="cuentas"
    )
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    #estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="PENDIENTE")
    tipo_cuenta=models.CharField(max_length=20, choices=TIPO_CUENTA_CHOICES, editable=False)
    observaciones = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def clean(self):
        """Validar que solo tenga una referencia válida según el tipo."""
        if self.trabajo_id and self.servicio_adicional_id:
            raise ValidationError(
                "Una cuenta no puede estar asociada a trabajo y servicio al mismo tiempo."
            )

        if not self.trabajo_id and not self.servicio_adicional_id:
            raise ValidationError(
                "La cuenta debe estar asociada a un trabajo o a un servicio adicional."
            )

    def _generar_numero_cuenta(self):
        from datetime import datetime

        year = datetime.now().year
        prefijo = f"CT-{year}"
        ultima = (
            CuentaCobrar.objects.filter(numero_cuenta__startswith=prefijo)
            .order_by("-id")
            .first()
        )
        siguiente = 1
        if ultima:
            try:
                siguiente = int(ultima.numero_cuenta.split("-")[-1]) + 1
            except (ValueError, IndexError):
                siguiente = 1
        return f"{prefijo}-{siguiente:04d}"

    def save(self, *args, **kwargs):
        # tipo_cuenta se derivaba en clean(), que DRF nunca llama: quedaba vacío.
        if self.trabajo_id:
            self.tipo_cuenta = "TRABAJO"
        elif self.servicio_adicional_id:
            self.tipo_cuenta = "SERVICIO"

        # El número vivía solo en el serializer: las cuentas creadas por ORM
        # quedaban con numero_cuenta='' y chocaban con el unique entre ellas.
        if not self.numero_cuenta:
            self.numero_cuenta = self._generar_numero_cuenta()

        super().save(*args, **kwargs)

    @property
    def total_pagado(self):
        return self.pagos.aggregate(
            total=Sum("monto")
        )["total"] or Decimal("0.00")
    @property
    def saldo_pendiente(self):
        return Decimal(self.monto_total) - self.total_pagado
    
    @property
    def estado_pago(self):
        if self.saldo_pendiente <= 0:
            return "PAGADO"
        elif self.total_pagado > 0:
            return "PARCIAL"
        return "PENDIENTE"
    
    def __str__(self):
        return f"{self.numero_cuenta} - {self.cliente}"