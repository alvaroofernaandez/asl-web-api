from rest_framework import serializers
from ..Models.ProyectoModel import Proyecto

class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = ['id', 'nombre', 'imagen', 'estado', 'descripcion', 'participantes','usuarios']

    # La siguiente funcion esta sobreescrita y permite validar los campos proporcionados en el viewset
    def is_valid(self, raise_exception=False):
        if not self.initial_data.get('usuarios', None):
            self.fields.pop('usuarios')  # Eliminamos usuarios si no es proporcionado por el usuario

        return super().is_valid(raise_exception=raise_exception)