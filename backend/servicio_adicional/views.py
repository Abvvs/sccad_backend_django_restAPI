from django.shortcuts import render
from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import TipoServicio, ServicioAdicional, ServicioAdicionalDetalle
from .serializers import TipoServicioSerializer, ServicioAdicionalDetalleSerializer, ServicioAdicionalSerializer
from cuenta_cobrar.models import CuentaCobrar


class TipoServicioListView(generics.ListAPIView):
    """Listar tipos de servicios activos"""
    queryset = TipoServicio.objects.filter(estado=True)
    serializer_class = TipoServicioSerializer
    permission_classes = [IsAuthenticated]

class ServicioAdicionalListCreateView(generics.ListCreateAPIView):
    queryset = ServicioAdicional.objects.all().select_related('cliente').prefetch_related('detalles')
    serializer_class = ServicioAdicionalSerializer
    permission_classes = [IsAuthenticated]

    ordering_fields = ['fecha_servicio', 'created_at']
    ordering = ['-fecha_servicio']

    @transaction.atomic
    def perform_create(self, serializer):
        servicio = serializer.save()

        # Sin cliente no hay a quién cobrarle (CuentaCobrar.cliente es obligatorio):
        # el servicio queda como venta de mostrador, sin cuenta por cobrar.
        if servicio.cliente_id is None:
            return

        # tipo_cuenta lo deriva CuentaCobrar.save(); saldo_pendiente es una
        # propiedad calculada, no un campo, y pasarla reventaba la creación.
        CuentaCobrar.objects.create(
            servicio_adicional=servicio,
            cliente=servicio.cliente,
            monto_total=servicio.monto_total,
        )

class ServicioAdicionalDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServicioAdicional.objects.all().select_related('cliente').prefetch_related('detalles')
    serializer_class = ServicioAdicionalSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        """
        Recalcular totales automáticamente como ya manejas en el serializer.
        """
        servicio = serializer.save()
        servicio.calcular_totales()
        servicio.actualizar_estado_pago()