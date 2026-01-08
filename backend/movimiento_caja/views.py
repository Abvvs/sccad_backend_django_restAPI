# finanzas/views/movimiento_caja.py
from rest_framework import generics
from .models import MovimientoCaja
from .serializers import MovimientoCajaSerializer


class MovimientoCajaListCreateView(generics.ListCreateAPIView):
    queryset = MovimientoCaja.objects.all().order_by('-created_at')
    serializer_class = MovimientoCajaSerializer


class MovimientoCajaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MovimientoCaja.objects.all()
    serializer_class = MovimientoCajaSerializer
