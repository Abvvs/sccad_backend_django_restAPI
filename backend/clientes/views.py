from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Cliente
from .serializers import ClienteSerializer, ClienteChoicesSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class ClienteListCreateView (generics.ListCreateAPIView):
    queryset = Cliente.objects.filter(estado=True)
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return super().get_queryset()
    
class ClienteDeactivateView(generics.UpdateAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(estado=False)

class ClienteRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]

class ClienteChoicesView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        data = {
            "identificaciones": Cliente.IDENTIFICACION_CHOICES,
        }
        serializer = ClienteChoicesSerializer(data)
        return Response(serializer.data)