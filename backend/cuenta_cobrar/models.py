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
    trabajo = models.ForeignKey(
        Trabajo, on_delete=models.PROTECT, null=True, blank=True, related_name="cuentas"
    )
    servicio_adicional = models.ForeignKey(
        ServicioAdicional, on_delete=models.PROTECT, null=True, blank=True, related_name="cuentas"
    )
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="PENDIENTE")
    observaciones = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def clean(self):
        """Validar que solo tenga una referencia válida según el tipo."""
        if self.tipo_cuenta == "TRABAJO":
            if not self.trabajo or self.servicio_adicional:
                raise ValidationError("Cuenta tipo TRABAJO debe tener trabajo_id y no servicio_id.")

        if self.tipo_cuenta == "SERVICIO":
            if not self.servicio_adicional or self.trabajo:
                raise ValidationError("Cuenta tipo SERVICIO debe tener servicio_id y no trabajo_id.")

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