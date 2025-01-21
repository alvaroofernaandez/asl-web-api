from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError('El correo electrónico debe ser proporcionado')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    ADMIN = 'admin'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Administrador'),
        (USER, 'Usuario normal')
    ]

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nombre")
    email = models.EmailField(unique=True, blank=False, null=False)
    password = models.CharField(max_length=128, null=False, verbose_name="Contraseña")
    role = models.CharField(max_length=10, choices=ROLES, default=USER)
    imagen = models.ImageField(upload_to='imagenes/',blank=True, null=True)
    antiguedad = models.DateField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def clean(self):
        # Comprobamos que todos los campos esten rellenos
        if not all([self.username, self.email, self.password]):
            raise ValidationError('Todos los campos deben estar rellenos correctamente.')

        # Validamos el correo con la funcion ya predefinida
        email_validator = EmailValidator()
        try:
            email_validator(self.email)
        except ValidationError as e:
            raise ValidationError("El correo electrónico no es válido.") from e

    def __str__(self):
        return self.username if self.username else self.email