from django.db import models
from rest_framework.exceptions import ValidationError


class User(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, null=False, verbose_name="Nombre")
    email = models.EmailField(unique=True, null=False, verbose_name="Correo Electrónico")
    password = models.CharField(max_length=128, null=False, verbose_name="Contraseña")

    def clean(self):
        if not all([self.nombre, self.email, self.password]):
            raise ValidationError('Todos los campos deben estar rellenados correctamente.')

    def __str__(self):
        return self.nombre
