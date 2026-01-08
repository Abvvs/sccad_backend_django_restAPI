from django.db import models

class EstadoTrabajo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    es_estado_final = models.BooleanField(default=False)
    color_hex = models.CharField(max_length=7, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Estado de trabajo"
        verbose_name_plural = "Estados de trabajo"

    def __str__(self):
        return self.nombre
    
class TipoTrabajo(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    incluye_campo = models.BooleanField(default=False)
    incluye_oficina = models.BooleanField(default=False)
    requiere_tramite = models.BooleanField(default=False)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Tipo de trabajo"
        verbose_name_plural = "Tipos de trabajo"

    def __str__(self):
        return self.nombre
    
class FormaPago(models.Model):
    FORMAS = [
        ('EFECTIVO', 'Efectivo'),
        ('TRANSFERENCIA', 'Transferencia'),
        ('CHEQUE', 'Cheque'),
        ('DEPOSITO', 'Depósito'),
        ('OTRO', 'Otro'),
    ]
    nombre = models.CharField(max_length=50, unique=True, choices=FORMAS)
    requiere_referencia = models.BooleanField(default=False)
    es_efectivo = models.BooleanField(default=False)
    estado = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Forma de pago"
        verbose_name_plural = "Formas de pago"

    def __str__(self):
        return self.nombre