from django.urls import path
from . import views
urlpatterns = [

    #principales
    path("", views.TrabajoListCreateView.as_view(), name="lista_trabajo"),
    path("<int:pk>/inactivar/", views.TrabajoDeactivateView.as_view(), name="trabajo_inactivar"),
    path("<int:pk>/", views.TrabajoRetrieveUpdateView.as_view(), name="tranajo_update"),
    path("catalogos/tipo-trabajo/", views.TipoTrabajoListView.as_view(), name="tipo_trabajo_list"),
    path("buscar/", views.buscar_trabajo, name="buscar_trabajo"),

    #historial
    path('<int:trabajo_id>/historial/', views.TrabajoHistorialListView.as_view(), name='trabajo_historial_list'),
    path('<int:trabajo_id>/historial/create/', views.TrabajoHistorialCreateView.as_view(), name='trabajo_historial_create'),

    # Clientes del trabajo
    path('<int:trabajo_id>/clientes/', views.TrabajoClientesView.as_view(), name='trabajo_clientes'),
    path('<int:trabajo_id>/clientes/agregar/', views.TrabajoClienteCreateView.as_view(), name='trabajo_cliente_agregar'),
    path('<int:trabajo_id>/clientes/<int:pk>/eliminar/', views.TrabajoClienteDeleteView.as_view(), name='trabajo_cliente_eliminar'),
    # Choices y búsqueda
    path('choices/', views.trabajos_choices, name='trabajos_choices'),
]