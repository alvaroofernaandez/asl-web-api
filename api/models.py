from django.db import models
from django.db.models import Model


class User(models.Model):
    idUser = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, null=False)
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(null=False)


    def str(self):
        return self.username

