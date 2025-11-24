from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from empleados.models import Empleado

class TestEmpleadoViews(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username = "test", password = "123456")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Crear empleado de prueba
        self.empleado = Empleado.objects.create(
            nombre="Juan",
            cedula_ruc="1234567890",
            telefono="0980270157",
            cuenta_bancaria="2212023599",
            banco="BANCO PICHINCA",
            estado=True,
        )
    def test_list_empleados_GET(self):
        url = reverse("lista_empleado")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nombre'], 'Juan')
    
    def test_create_empleado_POST(self):
        url = reverse("lista_empleado")
        data = {
            "nombre":"Maria",
            "cedula_ruc":"1234567891",
            "telefono":"0980270157",
            "cuenta_bancaria":"2212023599",
            "banco":"BANCO PICHINCA",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["nombre"], "Maria")
        self.assertTrue(Empleado.objects.filter(nombre="Maria").exists())
    
    def test_retrieve_empleado_GET(self):
        url = reverse('empleado_update', args=[self.empleado.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nombre"], "Juan")
    
    def test_update_empleado_PATCH(self):
        url = reverse("empleado_update", args=[self.empleado.id])
        data = {"nombre":"Juan actualizado"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.empleado.refresh_from_db()
        self.assertEqual(self.empleado.nombre, "Juan actualizado")
    
    def test_inactivar_empleado_PATCH(self):
        url = reverse("empleado_update", args=[self.empleado.id])
        response = self.client.patch(url,{"estado": False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.empleado.refresh_from_db()
        self.assertFalse(self.empleado.estado)