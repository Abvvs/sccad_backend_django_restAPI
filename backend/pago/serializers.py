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

    def validate(self, attrs):
        """
        Replica la regla de Pago.clean(): DRF no llama full_clean(), así que la
        validación del saldo tiene que vivir aquí para que realmente se aplique.
        """
        cuenta = attrs.get("cuenta_cobrar") or getattr(self.instance, "cuenta_cobrar", None)
        monto = attrs.get("monto", getattr(self.instance, "monto", None))

        if cuenta is not None and monto is not None:
            disponible = cuenta.saldo_pendiente
            # Al editar, el monto actual de este mismo pago vuelve a estar disponible.
            if self.instance is not None and self.instance.cuenta_cobrar_id == cuenta.id:
                disponible += self.instance.monto

            if monto > disponible:
                raise serializers.ValidationError({
                    "monto": f"El pago excede el saldo pendiente de la cuenta (${disponible})."
                })

        return attrs

    def _datos_movimiento(self, pago):
        return {
            "forma_pago": pago.forma_pago,
            "monto": pago.monto,
            "concepto": f"Pago cuenta #{pago.cuenta_cobrar_id}",
            "responsable": pago.recibido_por,
            "observaciones": pago.observaciones,
        }

    @transaction.atomic
    def create(self, validated_data):
        pago = Pago.objects.create(**validated_data)
        MovimientoCaja.objects.create(
            pago=pago,
            tipo_movimiento="INGRESO",
            **self._datos_movimiento(pago),
        )
        return pago

    @transaction.atomic
    def update(self, instance, validated_data):
        pago = super().update(instance, validated_data)
        # Mantiene la caja sincronizada con el pago editado.
        pago.movimientos_caja.update(**self._datos_movimiento(pago))
        return pago
