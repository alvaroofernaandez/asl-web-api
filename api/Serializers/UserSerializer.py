from rest_framework import serializers

from ..ViewSets.UserViewSet import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nombre', 'email', 'password', 'proyectos']