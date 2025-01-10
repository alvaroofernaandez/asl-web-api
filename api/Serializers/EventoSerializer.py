from rest_framework import serializers
from ..Models.TallerModel import Taller

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taller
        fields = ['id', 'nombre']