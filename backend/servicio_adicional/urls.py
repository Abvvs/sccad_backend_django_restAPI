from django.urls import path
from . import views

urlpatterns = [
    path('tipos-servicio/', views.TipoServicioListView.as_view(), name='tipos_servicios'),
    path('servicios/', views.ServicioAdicionalListCreateView.as_view(), name='lista_servicio_adicional'),
    path('servicios/<int:pk>/', views.ServicioAdicionalDetailView.as_view(), name='lista_servicio_adicional_detalle'),
]