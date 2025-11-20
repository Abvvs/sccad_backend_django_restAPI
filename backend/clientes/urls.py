from django.urls import path
from . import views
urlpatterns = [
    path("", views.ClienteListCreateView.as_view(), name="lista_cliente"),
    path('<int:pk>/inactivar/', views.ClienteDeactivateView.as_view(), name='cliente_inactivar'),
    path('<int:pk>/', views.ClienteRetrieveUpdateView.as_view(), name='cliente_update'),
    path("choices/", views.ClienteChoicesView.as_view(), name="cliente_choices"),
]