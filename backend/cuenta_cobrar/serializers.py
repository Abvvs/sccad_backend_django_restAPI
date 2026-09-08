from rest_framework import serializers
from .models import CuentaCobrar
from pago.serializers import PagoSerializer


class CuentaCobrarSerializer(serializers.ModelSerializer):
    cliente = serializers.CharField(
        source="cliente.nombre", read_only=True
    )
    trabajo_numero = serializers.CharField(source="trabajo.numero_trabajo", read_only=True)
    servicio_numero = serializers.CharField(source="servicio_adicional.numero_servicio", read_only=True)
    pagos = PagoSerializer(many=True, read_only=True)
    class Meta:
        model = CuentaCobrar
        fields = [
            "id",
            "numero_cuenta",
            "pagos",
            "tipo_cuenta",
            "trabajo",
            "servicio_adicional",
            "cliente",
            "monto_total",
            "saldo_pendiente",
            "estado_pago",
            "observaciones",
            "created_at",
            "updated_at",
            "servicio_numero",
            "trabajo_numero",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def validate(self, data):
        # tipo_cuenta es editable=False (read_only en DRF), así que nunca llega en
        # los datos: el tipo se deduce de la referencia enviada.
        trabajo = data.get("trabajo", getattr(self.instance, "trabajo", None))
        servicio = data.get("servicio_adicional", getattr(self.instance, "servicio_adicional", None))

        if trabajo and servicio:
            raise serializers.ValidationError(
                "Una cuenta no puede estar asociada a un trabajo y a un servicio adicional a la vez."
            )

        if not trabajo and not servicio:
            raise serializers.ValidationError(
                "La cuenta debe estar asociada a un trabajo o a un servicio adicional."
            )

        return data
