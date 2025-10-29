from django.db import models
from django.core.validators import RegexValidator

class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    cedula_ruc = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Cédula',
        validators=[
            RegexValidator(
                regex=r'^\d{10}$|^\d{13}$',
                message='La cédula debe tener 10 o 13 dígitos',
            )
        ],
        help_text='Número de cédula única'
    )
    telefono = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',  # solo 10 dígitos
                message="Ingrese un número de teléfono válido de 10 dígitos"
            )
        ], 
        blank=True, 
        null=True
    )
    cuenta_bancaria = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Número de cuenta bancaria',
        help_text='Número de cuenta para pagos'
    )
    banco = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Banco',
        help_text='Nombre del banco'
    )
    estado = models.BooleanField(default=True) # activo_inactivo
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nombre
