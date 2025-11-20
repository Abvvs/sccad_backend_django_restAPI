from rest_framework import serializers
from .models import Trabajo, TrabajoCliente, EstadoTrabajo, TipoTrabajo, TrabajoEstadoHistorial

class EstadoTrabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoTrabajo
        fields = ["id", "nombre","es_estado_final" ,"color_hex"]

class TipoTrabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoTrabajo
        fields = ["id", "nombre", "incluye_campo", "incluye_oficina", "requiere_tramite"]

class TrabajoEstadoHistorialSerializer(serializers.ModelSerializer):
    estado_trabajo_nombre = serializers.CharField(source= 'estado_trabajo.nombre', read_only = True)

    class Meta:
        model = TrabajoEstadoHistorial
        fields = [
            'id', 'trabajo', 'estado_trabajo', 'estado_trabajo_nombre',
            'fecha_cambio', 'usuario_responsable', 'departamento_actual',
            'observaciones', 'documentos_requeridos', 'fecha_estimada_siguiente_paso',
            'created_at'
        ]
        read_only_fields = ['trabajo', 'fecha_cambio', 'created_at']

class TrabajoClienteSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)
    cliente_telefono = serializers.CharField(source='cliente.telefono', read_only=True)
    
    class Meta:
        model = TrabajoCliente
        fields = [
            'id', 'cliente', 'cliente_nombre', 'cliente_telefono',
            'tipo_etiqueta', 'observaciones', 'created_at'
        ]

class TrabajoSerializer(serializers.ModelSerializer):
    tipo_trabajo_nombre = serializers.CharField(source='tipo_trabajo.nombre', read_only=True)
    estado_trabajo_nombre = serializers.CharField(source='estado_trabajo_actual.nombre', read_only=True)
    estado_pago_display = serializers.CharField(source='get_estado_pago_display', read_only=True)
    tipo_trabajo = TipoTrabajoSerializer(read_only=True)
    estado_actual = EstadoTrabajoSerializer(source="estado_trabajo_actual", read_only=True)

    tipo_trabajo_id = serializers.PrimaryKeyRelatedField(
        queryset=TipoTrabajo.objects.all(),
        source="tipo_trabajo",
        write_only=True,
        required=True,
    )
    clientes_relacionados = TrabajoClienteSerializer(source='clientes_relacionadas', many=True, read_only=True)
    class Meta:
        model = Trabajo
        fields = [
            'id', 'numero_trabajo', 'tipo_trabajo', 'tipo_trabajo_id', 
            'tipo_trabajo_nombre',
            'descripcion', 'direccion_campo',
            'monto_total', 'saldo_pendiente', 'estado_pago', 'estado_pago_display',
            'estado_trabajo_actual', 'estado_trabajo_nombre', 
            'estado_actual','observaciones', 'activo', 'created_at', 'updated_at',
            'clientes_relacionados'
        ]

        read_only_fields = ['numero_trabajo', 'created_at', 'updated_at']
    def create(self, validated_data):
    # Generar número de trabajo automáticamente
        ultimo_trabajo = Trabajo.objects.order_by('-id').first()
        if ultimo_trabajo and ultimo_trabajo.numero_trabajo:
            try:
                ultimo_numero = int(ultimo_trabajo.numero_trabajo.split('-')[-1])
                nuevo_numero = f"SCCAD-2025-{str(ultimo_numero + 1).zfill(3)}"
            except:
                nuevo_numero = "SCCAD-2025-001"
        else:
            nuevo_numero = "SCCAD-2025-001"
        
        validated_data['numero_trabajo'] = nuevo_numero
        return super().create(validated_data)