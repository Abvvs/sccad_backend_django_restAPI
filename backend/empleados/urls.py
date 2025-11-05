from django.urls import path
from . import views
urlpatterns = [
    path("", views.EmpleadoListCreateView.as_view(), name="lista_empleado"),
    path('<int:pk>/inactivar/', views.EmpleadoDeactivateView.as_view(), name='empleado_inactivar'),
    path('<int:pk>/', views.EmpleadoRetrieveUpdateView.as_view(), name='empleado_update'),
]
