from django.urls import path
from .views import *

urlpatterns = [
    path("", MovimientoCajaListCreateView.as_view(), name="movimientos-caja-list-create"),
    path("<int:pk>/", MovimientoCajaDetailView.as_view(), name="movimientos-caja-detail"),
]