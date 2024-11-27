from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import User
from..Serializers.UserSerializer import UserSerializer

class UserViewSet(APIView):
    #Mediante el siguiente metodo obtenemos todos los usuarios
    def get(self,request):
        #Obtenemos todos los usuarios y luego los pasamos a formato json
        usuarios = User.objects.all()
        serializer = UserSerializer(usuarios, many=True)
        return Response(serializer.data)

    #Mediante este metodo vamos a poder añadir un usuario
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)