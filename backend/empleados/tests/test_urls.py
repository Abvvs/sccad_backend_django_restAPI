from django.test import SimpleTestCase
from django.urls import reverse, resolve
from empleados.views import (
    EmpleadoListCreateView,
    EmpleadoDeactivateView,
    EmpleadoRetrieveUpdateView,
)

class TestEmpleadoUrls(SimpleTestCase):
    def test_lista_empleado_url_resolves(self):
        url = reverse("lista_empleado")
        resolved = resolve(url)
        self.assertEqual(resolved.func.view_class, EmpleadoListCreateView)

    def test_empleado_inactivar_url_resolves(self):
        url = reverse("empleado_inactivar", args=[1])
        resolved = resolve(url)
        self.assertEqual(resolved.func.view_class, EmpleadoDeactivateView)

    def test_empleado_update_url_resolves(self):
        url = reverse("empleado_update", args=[1])
        resolved = resolve(url)
        self.assertEqual(resolved.func.view_class, EmpleadoRetrieveUpdateView)