from rest_framework import serializers
from .models import Cliente

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = [
            'id','nombre','razon_social','tipo_identificacion','identificacion','telefono', 'observaciones', 'estado'
        ]
    def validate_cedula_ruc(self, value):
        # Si estamos editando, ignorar el mismo registro
        if self.instance:
            if Cliente.objects.exclude(id=self.instance.id).filter(identificacion=value).exists():
                raise serializers.ValidationError("Ya existe un Cliente con esta cédula.")
        else:
            # Si estamos creando
            if Cliente.objects.filter(identificacion=value).exists():
                raise serializers.ValidationError("Ya existe un Cliente con esta cédula.")
        return value

class ClienteChoicesSerializer(serializers.Serializer):
    identificaciones = serializers.ListField()