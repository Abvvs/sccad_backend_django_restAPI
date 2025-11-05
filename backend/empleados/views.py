from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Empleado
from .serializers import EmpleadoSerializer

class EmpleadoListCreateView(generics.ListCreateAPIView):
    queryset = Empleado.objects.filter(estado=True)
    serializer_class = EmpleadoSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return super().get_queryset()

class EmpleadoDeactivateView(generics.UpdateAPIView):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(estado=False)

class EmpleadoRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer
    permission_classes = [IsAuthenticated]
