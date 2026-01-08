# finanzas/serializers/movimiento_caja.py
from rest_framework import serializers
from .models import MovimientoCaja

class MovimientoCajaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientoCaja
        fields = '__all__'
