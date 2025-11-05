from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Trabajo, TipoTrabajo
from .serializers import TrabajoSerializer, TipoTrabajoSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def buscar_trabajo(request):
    query = request.GET.get("q", "").strip()

    if not query:
        return Response({"error": "Debe proporcionar un número de trabajo o nombre de propietario."}, status=400)

    trabajos = Trabajo.objects.filter(
        Q(numero_trabajo__icontains=query)
    ).distinct()
    if not trabajos.exists():
        return Response({"message": "No se encontraron trabajos con ese criterio."}, status=404)
    
    serializer = TrabajoSerializer(trabajos, many=True)
    return Response(serializer.data)

class TrabajoListCreateView(generics.ListCreateAPIView):
    queryset = Trabajo.objects.all().select_related("tipo_trabajo", "estado_trabajo_actual") #optimiza las consultas
    serializer_class = TrabajoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset()
    
    def perform_create(self, serializer):
        serializer.save(created_at=self.request.user)
    
class TrabajoDelete(generics.DestroyAPIView):
    queryset = Trabajo.objects.all()
    serializer_class = TrabajoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset()

class TipoTrabajoListView(generics.ListAPIView):
    queryset = TipoTrabajo.objects.all()
    serializer_class = TipoTrabajoSerializer


