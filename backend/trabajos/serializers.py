from rest_framework import serializers
from .models import Trabajo, TrabajoPersona, EstadoTrabajo, TipoTrabajo
class EstadoTrabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoTrabajo
        fields = ["id", "nombre", "color_hex"]

class TipoTrabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoTrabajo
        fields = ["id", "nombre", "incluye_campo", "incluye_oficina", "requiere_tramite"]

class TrabajoSerializer(serializers.ModelSerializer):
    tipo_trabajo = TipoTrabajoSerializer(read_only=True)
    estado_actual = EstadoTrabajoSerializer(source="estado_trabajo_actual", read_only=True)

    tipo_trabajo_id = serializers.PrimaryKeyRelatedField(
        queryset=TipoTrabajo.objects.all(),
        source="tipo_trabajo",
        write_only=True,
        required=False
    )
    class Meta:
        model = Trabajo
        fields = [
            "id", "numero_trabajo", "descripcion", "direccion_campo", "monto_total",
            "estado_pago", "prioridad", "tipo_trabajo", "tipo_trabajo_id", "estado_actual"
        ]