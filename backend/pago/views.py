from rest_framework import generics
from .models import Pago
from .serializers import PagoSerializer


class PagoListCreateView(generics.ListCreateAPIView):
    queryset = Pago.objects.all().order_by("-created_at")
    serializer_class = PagoSerializer


class PagoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer

    def perform_destroy(self, instance):
        # Revertir pago antes de eliminar
        instance.revertir_pago()
        instance.delete()
