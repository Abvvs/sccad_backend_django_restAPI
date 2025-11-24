from django.test import TestCase
from django.core.exceptions import ValidationError
from empleados.models import Empleado

class testEmpleadoModel(TestCase):
    def setUp(self):
        self.empleado = Empleado.objects.create(
            nombre="Juan Pérez",
            cedula_ruc="1234567890",
            telefono="0987654321",
            cuenta_bancaria="123456789",
            banco="Banco Pichincha"
        )

    def test_creacion_empleado(self):
        """Debe crear un empleado correctamente."""
        self.assertEqual(self.empleado.nombre, "Juan Pérez")
        self.assertEqual(self.empleado.cedula_ruc, "1234567890")
        self.assertEqual(self.empleado.telefono, "0987654321")
        self.assertTrue(self.empleado.estado)  # valor por defecto

    def test_str(self):
        """__str__ debe devolver el nombre."""
        self.assertEqual(str(self.empleado), "Juan Pérez")

    def test_validacion_cedula_invalida(self):
        """Debe fallar si la cédula no tiene 10 o 13 dígitos."""
        empleado = Empleado(
            nombre="Pedro",
            cedula_ruc="12345",  # inválido
            telefono="0987654321"
        )
        with self.assertRaises(ValidationError):
            empleado.full_clean()  # activa las validaciones

    def test_validacion_cedula_13_digitos(self):
        """Debe aceptar cédula de 13 dígitos."""
        empleado = Empleado(
            nombre="Ana",
            cedula_ruc="1234567890123",
            telefono="0987654321"
        )
        # No debería lanzar error
        empleado.full_clean()

    def test_validacion_telefono_invalido(self):
        """Debe fallar si el teléfono no tiene 10 dígitos."""
        empleado = Empleado(
            nombre="Luis",
            cedula_ruc="1234567890",
            telefono="1234"  # inválido
        )
        with self.assertRaises(ValidationError):
            empleado.full_clean()

    def test_timestamps(self):
        """Debe guardarse fecha_creacion y fecha_actualizacion."""
        self.assertIsNotNone(self.empleado.fecha_creacion)
        self.assertIsNotNone(self.empleado.fecha_actualizacion)