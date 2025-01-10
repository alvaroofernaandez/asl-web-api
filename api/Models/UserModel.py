from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, null=False, verbose_name="Nombre")
    email = models.EmailField(unique=True, null=False, verbose_name="Correo Electrónico")
    password = models.CharField(max_length=128, null=False, verbose_name="Contraseña")

    '''
        Las siguientes dos funciones permiten tanto hashear como comprobar si las contraseñas son correctas
        set_password establece la contraseña hasheada y check_password comprueba que es correcta
    '''
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self,raw_password):
        return check_password(raw_password,self.password)
    def clean(self):
        # Validamos que todos los campos estan rellenos
        if not all([self.nombre, self.email, self.password]):
            raise ValidationError('Todos los campos deben estar rellenados correctamente.')

        # Validamos el correo electrónico con EmailValidator
        email_validator = EmailValidator()
        try:
            email_validator(self.email)  # Lanzamos un ValidationError (error) si el correo no es válido
        except ValidationError as e:
            raise ValidationError("El correo electrónico no es válido.") from e

    def __str__(self):
        return self.nombre
