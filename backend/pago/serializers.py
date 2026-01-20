from rest_framework import serializers
from .models import Pago
from django.db import transaction
from movimiento_caja.models import MovimientoCaja



class PagoSerializer(serializers.ModelSerializer):
    forma_pago_nombre = serializers.CharField(source="forma_pago.nombre", read_only=True)
    class Meta:
        model = Pago
        fields = [
            "id",
            "cuenta_cobrar",
            "fecha_pago",
            "forma_pago",
            "forma_pago_nombre",
            "monto",
            "observaciones",
            "recibido_por",
            "created_at",
        ]
        read_only_fields = ["created_at"]

    def validate_monto(self, value):
        if value <= 0:
            raise serializers.ValidationError("El monto debe ser mayor a cero.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        pago = Pago.objects.create(**validated_data)
        MovimientoCaja.objects.create(
            pago=pago,
            tipo_movimiento="INGRESO",
            forma_pago=pago.forma_pago,
            monto=pago.monto,
            concepto=f"Pago cuenta #{pago.cuenta_cobrar.id}",
            responsable=pago.recibido_por,
            observaciones=pago.observaciones,
        )
        return pago
