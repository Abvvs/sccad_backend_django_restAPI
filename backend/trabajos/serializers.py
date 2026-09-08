from rest_framework import serializers
from .models import Trabajo, TrabajoCliente, EstadoTrabajo, TipoTrabajo, TrabajoEstadoHistorial, FormaPago, AsignacionTrabajo
from django.utils import timezone
from cuenta_cobrar.serializers import CuentaCobrarSerializer

class EstadoTrabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoTrabajo
        fields = ["id", "nombre","es_estado_final" ,"color_hex"]

class TipoTrabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoTrabajo
        fields = ["id", "nombre", "incluye_campo", "incluye_oficina", "requiere_tramite"]
class FormaPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormaPago
        fields = ["id", "nombre", "es_efectivo"]
class TrabajoEstadoHistorialSerializer(serializers.ModelSerializer):
    estado_trabajo_nombre = serializers.CharField(source= 'estado_trabajo.nombre', read_only = True)

    class Meta:
        model = TrabajoEstadoHistorial
        fields = [
            'id', 'trabajo', 'estado_trabajo', 'estado_trabajo_nombre',
            'fecha_cambio', 'usuario_responsable', 'departamento_actual',
            'observaciones', 'fecha_estimada_siguiente_paso',
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
    cuenta = CuentaCobrarSerializer(read_only=True)
    estado_pago = serializers.CharField(source="cuenta.estado_pago", read_only=True)
    tipo_trabajo = TipoTrabajoSerializer(read_only=True)
    estado_actual = EstadoTrabajoSerializer(source="estado_trabajo_actual", read_only=True)
    historial = TrabajoEstadoHistorialSerializer(source='historial_estados', many=True, read_only=True)
    saldo_pendiente = serializers.DecimalField(source="cuenta.saldo_pendiente", max_digits=10, decimal_places=2, read_only=True)
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
            'monto_total', 'saldo_pendiente', 'estado_pago',
            'estado_trabajo_actual', 'estado_trabajo_nombre', 
            'estado_actual','observaciones', 'estado', 'created_at', 'updated_at',
            'clientes_relacionados', 'historial', 'cuenta',
        ]

        read_only_fields = ['numero_trabajo', 'created_at', 'updated_at']
    def create(self, validated_data):
    # Generar número de trabajo automáticamente
        anio_actual = timezone.now().year
        prefijo = f"SCCAD-{anio_actual}"
        ultimo_trabajo_anio = Trabajo.objects.filter(
            numero_trabajo__startswith=prefijo
        ).order_by('-id').first()
        if ultimo_trabajo_anio and ultimo_trabajo_anio.numero_trabajo:
            try:
                ultimo_numero_str = ultimo_trabajo_anio.numero_trabajo.split('-')[-1]
                nuevo_numero_int = int(ultimo_numero_str) + 1
                nuevo_numero = f"{prefijo}-{str(nuevo_numero_int).zfill(3)}"
            except(ValueError, IndexError):
                # Por si acaso el formato falla, empezamos en 001
                nuevo_numero = f"{prefijo}-001"
        else:
            # Si es el primer trabajo del año
            nuevo_numero = f"{prefijo}-001"
        
        validated_data['numero_trabajo'] = nuevo_numero
        return super().create(validated_data)

class AsignacionTrabajoSerializer(serializers.ModelSerializer):
    empleado_nombre = serializers.CharField( source="empleado.nombre", read_only=True)
    trabajo_codigo = serializers.CharField( source="trabajo.numero_trabajo", read_only=True)
    trabajo_descripcion = serializers.CharField(source="trabajo.descripcion", read_only=True)
    fecha = serializers.DateField(input_formats=["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S"])
    trabajo_tipo_trabajo = serializers.CharField( source="trabajo.tipo_trabajo", read_only=True)
    rol_nombre = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()
    total_a_pagar = serializers.SerializerMethodField()
    class Meta:
        model = AsignacionTrabajo
        fields = "__all__"

    def get_rol_nombre(self, obj):
        return obj.get_rol_display()
    def get_subtotal(self, obj):
        return float(obj.subtotal)

    def get_total_a_pagar(self, obj):
        return float(obj.total_a_pagar)
