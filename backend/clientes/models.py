from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

# Create your models here.
class Cliente(models.Model):
    
    IDENTIFICACION_CHOICES = [
        ('CEDULA', 'Cédula'),
        ('RUC', 'Ruc'),
        ('PASAPORTE', 'Pasaporte'),
    ]

    nombre = models.CharField(max_length=100,help_text="Nombres del cliente")
    razon_social = models.CharField(max_length=100,blank=True)
    tipo_identificacion =  models.CharField(max_length=20, choices= IDENTIFICACION_CHOICES, blank=True, null= True)
    identificacion = models.CharField (max_length=20, help_text= 'Número de identificación', null= True, blank=True, unique=True)
    telefono = models.CharField(max_length=15, blank=True,validators= [RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message='Ingrese un número de teléfono válido'
    )])
    observaciones = models.TextField(
        blank=True,
        help_text="Observaciones o notas adicionales"
    )
    estado = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Indica si la persona está activa en el sistema"
    )
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nombre

    
