from django.urls import path
from . import views
urlpatterns = [
    path("", views.TrabajoListCreateView.as_view(), name="lista_trabajo"),
    path("buscar/", views.buscar_trabajo, name="buscar_trabajo"),
    path("eliminar/<int:pk>/", views.TrabajoDelete.as_view(), name="eliminar_trabajo"),
    path("catalogos/tipo-trabajo/", views.TipoTrabajoListView.as_view(), name="tipo_trabajo_list"),
]