from rest_framework import serializers
from .models import Pago


class PagoSerializer(serializers.ModelSerializer):
    cuenta_numero = serializers.CharField(
        source="cuenta_cobrar.numero_cuenta", read_only=True
    )

    class Meta:
        model = Pago
        fields = [
            "id",
            "cuenta_cobrar",
            "cuenta_numero",
            "fecha_pago",
            "forma_pago",
            "monto",
            "referencia",
            "banco",
            "numero_cheque",
            "observaciones",
            "recibido_por",
            "created_at",
        ]
        read_only_fields = ["created_at"]

    def validate_monto(self, value):
        if value <= 0:
            raise serializers.ValidationError("El monto debe ser mayor a cero.")
        return value

    def create(self, validated_data):
        pago = Pago.objects.create(**validated_data)
        pago.aplicar_pago()
        return pago

    def update(self, instance, validated_data):
        # Revertir primero el pago anterior
        instance.revertir_pago()

        # Actualizar el pago
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Volver a aplicar el nuevo pago
        instance.aplicar_pago()

        return instance
