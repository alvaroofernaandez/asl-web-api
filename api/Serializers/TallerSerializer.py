from rest_framework import serializers
from ..Models.TallerModel import Taller

class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taller
        fields = ['id', 'nombre']