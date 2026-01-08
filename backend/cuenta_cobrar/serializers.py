from rest_framework import serializers
from .models import CuentaCobrar


class CuentaCobrarSerializer(serializers.ModelSerializer):
    cliente = serializers.CharField(
        source="cliente.nombre", read_only=True
    )
    trabajo_numero = serializers.CharField(source="trabajo.numero_trabajo", read_only=True)
    servicio_numero = serializers.CharField(source="servicio_adicional.numero_servicio", read_only=True)

    class Meta:
        model = CuentaCobrar
        fields = [
            "id",
            "numero_cuenta",
            "tipo_cuenta",
            "trabajo",
            "trabajo_numero",
            "servicio_adicional",
            "servicio_numero",
            "cliente",
            "monto_total",
            "saldo_pendiente",
            "estado",
            "observaciones",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def validate(self, data):
        tipo = data.get("tipo_cuenta", self.instance.tipo_cuenta if self.instance else None)
        trabajo = data.get("trabajo", getattr(self.instance, "trabajo", None) if self.instance else None)
        servicio = data.get("servicio_adicional", getattr(self.instance, "servicio_adicional", None) if self.instance else None)

        if tipo == "TRABAJO":
            if not trabajo or servicio:
                raise serializers.ValidationError("Cuenta tipo TRABAJO requiere trabajo_id y no servicio_adicional_id.")

        if tipo == "SERVICIO":
            if not servicio or trabajo:
                raise serializers.ValidationError("Cuenta tipo SERVICIO requiere servicio_adicional_id y no trabajo_id.")

        return data
    def create(self, validated_data):
        # generar número de cuenta
        from datetime import datetime
        year = datetime.now().year

        last_cuenta = CuentaCobrar.objects.filter(
            numero_cuenta__startswith=f"CT-{year}"
        ).order_by("-id").first()

        if last_cuenta:
            last_num = int(last_cuenta.numero_cuenta.split("-")[-1])
            new_num = last_num + 1
        else:
            new_num = 1

        validated_data["numero_cuenta"] = f"CT-{year}-{new_num:04d}"

        return super().create(validated_data)
