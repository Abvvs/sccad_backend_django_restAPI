from django.db import models
from trabajos.models import Trabajo
from empleados.models import Empleado

class TarifaRol(models.Model):
    TOPOGRAFO = 1
    CADENERO = 2
    SOLO_CARRERA = 3
    CHOICES_ROLES = [
        (TOPOGRAFO, "Topógrafo"),
        (CADENERO, "Cadenero"),
        (SOLO_CARRERA, "Solo Carrera"),
    ]
    rol = models.IntegerField(choices=CHOICES_ROLES, unique=True)
    tarifa_dia = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.get_rol_display()} - ${self.tarifa_dia}/día"

    class Meta:
        verbose_name = "Tarifa por Rol"
        verbose_name_plural = "Tarifas por Rol"

class AsignacionTrabajo(models.Model):
    TOPOGRAFO = 1
    CADENERO = 2
    SOLO_CARRERA = 3
    CHOICES_ROLES = [
        (TOPOGRAFO, "Topógrafo"),
        (CADENERO, "Cadenero"),
        (SOLO_CARRERA, "Solo Carrera"),
    ]
    trabajo = models.ForeignKey(Trabajo, on_delete=models.CASCADE, related_name="asignaciones")
    empleado = models.ForeignKey(Empleado, on_delete=models.PROTECT, related_name="asignaciones")
    fecha = models.DateField()
    rol = models.IntegerField(choices=CHOICES_ROLES)
    carrera = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    personal_adicional_desc = models.CharField(max_length=100, null=True, blank=True)
    dias_trabajados = models.DecimalField(max_digits=3, decimal_places=1, default=1)
    costo_personal_adicional = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    adelanto = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    observaciones = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ("trabajo", "empleado", "fecha", "rol")
        ordering = ["-fecha"]
    
    # En el modelo
    @property
    def subtotal(self):
        try:
            tarifa = TarifaRol.objects.get(rol=self.rol)
            return self.dias_trabajados * tarifa.tarifa_dia
        except TarifaRol.DoesNotExist:
            return 0

    @property  
    def total_a_pagar(self):
        return self.subtotal + self.carrera + self.costo_personal_adicional - self.adelanto

    def __str__(self):
        return f"{self.fecha} - {self.empleado} → {self.trabajo} ({self.get_rol_display()})"