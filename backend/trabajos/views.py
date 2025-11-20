from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Trabajo, TipoTrabajo, TrabajoEstadoHistorial, EstadoTrabajo, TrabajoCliente
from .serializers import (
    TrabajoSerializer, 
    TipoTrabajoSerializer,
    TrabajoEstadoHistorialSerializer,
    EstadoTrabajoSerializer,
    TrabajoClienteSerializer
)

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
    queryset = Trabajo.objects.filter(activo=True).select_related("tipo_trabajo", "estado_trabajo_actual")
    serializer_class = TrabajoSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return super().get_queryset()
    

    def perform_create(self, serializer):
        serializer.save(created_at=self.request.user)

class TrabajoRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Trabajo.objects.all()
    serializer_class = TrabajoSerializer
    permission_classes = [IsAuthenticated]  

class TrabajoDeactivateView(generics.UpdateAPIView):
    queryset = Trabajo.objects.all()
    serializer_class = TrabajoSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(activo=False)

class TipoTrabajoListView(generics.ListAPIView):
    queryset = TipoTrabajo.objects.all()
    serializer_class = TipoTrabajoSerializer

#views del historial

class TrabajoHistorialListView(generics.ListAPIView):
    """GET /api/trabajos/{pk}/historial/ - Ver historial de un trabajo"""
    serializer_class = TrabajoEstadoHistorialSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        trabajo_id = self.kwargs['trabajo_id']
        return TrabajoEstadoHistorial.objects.filter(
            trabajo_id=trabajo_id
        ).select_related('estado_trabajo').order_by('-fecha_cambio')
    

class TrabajoHistorialCreateView(generics.CreateAPIView):
    """POST /api/trabajos/{pk}/historial/ - Agregar estado al historial"""
    serializer_class = TrabajoEstadoHistorialSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        trabajo_id = self.kwargs['trabajo_id']
        trabajo = Trabajo.objects.get(id=trabajo_id)
        
        # Guardar el historial
        historial = serializer.save(trabajo=trabajo, usuario_responsable=self.request.user.username)
        
        # Actualizar el estado actual del trabajo
        trabajo.estado_trabajo_actual = historial.estado_trabajo
        trabajo.save()

class TrabajoClientesView(APIView):
    """GET /api/trabajos/{pk}/clientes/ - Ver clientes de un trabajo"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, trabajo_id):
        try:
            trabajo = Trabajo.objects.get(id=trabajo_id)
            relaciones = trabajo.clientes_relacionadas.select_related('cliente')
            
            data = [{
                'id': rel.cliente.id,
                'nombre': rel.cliente.nombre,
                'identificacion': rel.cliente.identificacion,
                'telefono': rel.cliente.telefono,
                'tipo_etiqueta': rel.tipo_etiqueta_cliente,
                'observaciones': rel.observaciones
            } for rel in relaciones]
            
            return Response(data)
        except Trabajo.DoesNotExist:
            return Response(
                {'error': 'Trabajo no encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )
class TrabajoClienteCreateView (generics.CreateAPIView):
    serializer_class = TrabajoClienteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        trabajo_id = self.kwargs['trabajo_id']
        trabajo = Trabajo.objects.get(id=trabajo_id)
        serializer.save(trabajo=trabajo)

class TrabajoClienteDeleteView(generics.DestroyAPIView):
    """DELETE /api/trabajos/{trabajo_id}/clientes/{pk}/eliminar/ - Eliminar cliente del trabajo"""
    serializer_class = TrabajoClienteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        trabajo_id = self.kwargs['trabajo_id']
        return TrabajoCliente.objects.filter(trabajo_id=trabajo_id)

@api_view(['GET'])
@permission_classes([AllowAny])
def trabajos_choices(request):
    """GET /api/trabajos/choices/ - Opciones para formularios"""
    tipos_trabajo = TipoTrabajo.objects.filter(activo=True)
    estados_trabajo = EstadoTrabajo.objects.all()
    
    return Response({
        'tipos_trabajo': [[str(t.id), t.nombre] for t in tipos_trabajo],
        'estados_trabajo': [[str(e.id), e.nombre] for e in estados_trabajo],
        'estados_pago': Trabajo.ESTADO_PAGO,
    })