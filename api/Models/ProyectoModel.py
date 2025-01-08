from django.db import models
from django.core.exceptions import ValidationError

# Función para validar que los participantes sean mayores que 0
def validar_participantes(value):
    if value < 1:
        raise ValidationError('El número de participantes debe ser mayor que 0.')

class Proyecto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(blank=False, null=False, max_length=180)
    imagen = models.ImageField(upload_to='imagenes/', blank=False, null=False)
    estado = models.CharField(blank=False, null=False, max_length=180)
    descripcion = models.TextField(blank=False, null=False) # Textfield acepta una mayor cantidad de texto
    participantes = models.IntegerField(validators=[validar_participantes])  # Validamos participantes

    # Creamos una funcion para validar los campos y comprobar si están o no vacíos
    def clean(self):
        # Comprobamos si los campos están vacíos y devolverá un error
        if not all([self.nombre, self.imagen, self.estado, self.descripcion, self.participantes]):
            raise ValidationError('Todos los campos deben estar completos.')

        # Validamos los participantes
        self.validar_participantes()

    def validar_participantes(self):
        if self.participantes < 1:
            raise ValidationError('El número de participantes debe ser mayor que 0.')

    def __str__(self):
        return self.nombre
