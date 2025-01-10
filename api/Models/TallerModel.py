from django.db import models
from django.core.exceptions import ValidationError
from ..models import User

class Taller(models.Model):
    id = models.AutoField(primary_key=True) # No haría falta
    nombre = models.CharField(blank=False, null=False, max_length=180)
    usuarios = models.ManyToManyField(User, related_name='taller')

    # En esta funcion tenemos que validar los posibles campos vacios que hayan
    def clean(self):
        # Creamos un array con los campos que queramos que no estén vacíos
        content = [self.nombre]

        # Realizamos el control de errores para verificar que los campos esten rellenos
        if not all(content):
            raise ValidationError("Todos los campos deben de estar rellenos")

    def __str__(self):
        return self.nombre