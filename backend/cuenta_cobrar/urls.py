from django.urls import path
from .views import *

urlpatterns = [
    path("", CuentaCobrarListCreateView.as_view(), name="cuentas-list-create"),
    path("<int:pk>/", CuentaCobrarDetailView.as_view(), name="cuentas-detail"),
]