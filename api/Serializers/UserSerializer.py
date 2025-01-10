from rest_framework import serializers

from ..ViewSets.UserViewSet import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password','role']

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("This field may not be blank.")
        return value