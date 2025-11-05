from rest_framework import serializers
from .models import Empleado


class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = [
            'id','nombre','cedula_ruc','telefono', 'cuenta_bancaria', 'banco', 'estado'
        ]
    def validate_cedula_ruc(self, value):
        # Si estamos editando, ignorar el mismo registro
        if self.instance:
            if Empleado.objects.exclude(id=self.instance.id).filter(cedula_ruc=value).exists():
                raise serializers.ValidationError("Ya existe un empleado con esta cédula.")
        else:
            # Si estamos creando
            if Empleado.objects.filter(cedula_ruc=value).exists():
                raise serializers.ValidationError("Ya existe un empleado con esta cédula.")

        return value