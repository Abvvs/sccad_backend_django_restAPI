from rest_framework import generics
from .models import CuentaCobrar
from .serializers import CuentaCobrarSerializer


class CuentaCobrarListCreateView(generics.ListCreateAPIView):
    queryset = CuentaCobrar.objects.all().order_by("-created_at")
    serializer_class = CuentaCobrarSerializer


class CuentaCobrarDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CuentaCobrar.objects.all()
    serializer_class = CuentaCobrarSerializer