from rest_framework import serializers
from .models import TipoServicio, ServicioAdicional, ServicioAdicionalDetalle

class TipoServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoServicio
        fields = ['id', 'nombre', 'categoria', 'precio_unitario', 'unidad_medida', 'estado']

class ServicioAdicionalDetalleSerializer(serializers.ModelSerializer):
    tipo_servicio_nombre = serializers.CharField(
        source='tipo_servicio.nombre', 
        read_only=True
    )
    subtotal = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        read_only=True
    )

    class Meta:
        model = ServicioAdicionalDetalle
        fields = [
            'id',
            'tipo_servicio',
            'tipo_servicio_nombre',
            'cantidad',
            'precio_unitario',
            'subtotal',
            'descripcion'
        ]

    def validate(self, data):
        """Validar que cantidad y precio sean positivos"""
        if data.get('cantidad', 0) <= 0:
            raise serializers.ValidationError(
                {"cantidad": "La cantidad debe ser mayor a 0"}
            )
        if data.get('precio_unitario', 0) <= 0:
            raise serializers.ValidationError(
                {"precio_unitario": "El precio unitario debe ser mayor a 0"}
            )
        return data


class ServicioAdicionalSerializer(serializers.ModelSerializer):
    detalles = ServicioAdicionalDetalleSerializer(many=True)
    numero_servicio = serializers.CharField(read_only=True)
    monto_total = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        read_only=True
    )
    saldo_pendiente = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        read_only=True
    )
    estado_pago = serializers.CharField(read_only=True)

    class Meta:
        model = ServicioAdicional
        fields = [
            'id',
            'numero_servicio',
            'cliente',
            'fecha_servicio',
            'descripcion',
            'monto_total',
            'saldo_pendiente',
            'estado_pago',
            'observaciones',
            'detalles',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'numero_servicio', 
            'monto_total', 
            'saldo_pendiente',
            'estado_pago',
            'created_at', 
            'updated_at'
        ]

    def validate_detalles(self, value):
        """Validar que haya al menos un detalle"""
        if not value:
            raise serializers.ValidationError(
                "Debe incluir al menos un detalle de servicio"
            )
        return value

    def create(self, validated_data):
        """Crear servicio con sus detalles"""
        detalles_data = validated_data.pop('detalles')
        
        # Crear el servicio
        servicio = ServicioAdicional.objects.create(**validated_data)
        
        # Crear los detalles
        for detalle_data in detalles_data:
            ServicioAdicionalDetalle.objects.create(
                servicio_adicional=servicio,
                **detalle_data
            )
        
        # Calcular totales y establecer saldo inicial
        servicio.calcular_totales()
        servicio.saldo_pendiente = servicio.monto_total
        servicio.save()
        
        return servicio

    def update(self, instance, validated_data):
        """Actualizar servicio y sus detalles"""
        detalles_data = validated_data.pop('detalles', None)
        
        # Actualizar campos del servicio
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Si se enviaron detalles, reemplazarlos
        if detalles_data is not None:
            # Eliminar detalles existentes
            instance.detalles.all().delete()
            
            # Crear nuevos detalles
            for detalle_data in detalles_data:
                ServicioAdicionalDetalle.objects.create(
                    servicio_adicional=instance,
                    **detalle_data
                )
            
            # Recalcular totales
            instance.calcular_totales()
        
        return instance