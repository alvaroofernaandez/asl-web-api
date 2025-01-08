from rest_framework import serializers
from ..Models.ProyectoModel import Proyecto

class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = ['id', 'nombre', 'imagen', 'estado', 'descripcion', 'participantes']