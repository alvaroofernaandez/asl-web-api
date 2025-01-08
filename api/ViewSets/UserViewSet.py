from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from ..Models.UserModel import User
from ..Serializers.UserSerializer import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Metodo para obtener usuarios ordenados tanto por cantidad como por antiguedad
    @action(detail=False, methods=['get'])
    def get_pageable_users(self, request):
        cantidad_usuarios = request.query_params.get('cantidad', 3)  # Cantidad de usuarios por defecto es de 3
        try:
            cantidad_usuarios = int(cantidad_usuarios)
        except ValueError:
            cantidad_usuarios = 3  # Asignamos por defecto el valor de 3

        usuarios_filtrados = User.objects.all().order_by('-id')[:cantidad_usuarios]
        serializer = UserSerializer(usuarios_filtrados, many=True)
        return Response(serializer.data)

    # Método para crear usuarios
    @action(detail=False, methods=['post'])
    def create_user(self, request):
        # Recogemos en el cuerpo de la solicitud los datos
        nombre = request.data.get('nombre')
        email = request.data.get('email')
        password = request.data.get('password')

        # Validamos que los campos no están vacíos aunque el modelo ya lo incluye
        if not all([nombre, email, password]):
            return Response({'error': 'Todos los campos (nombre, email, password) son obligatorios.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # Creamos un nuevo usuario usando el serializer
            user = User.objects.create(
                nombre=nombre,
                email=email,
                password=password
            )

            return Response(
                {'success': 'Usuario creado correctamente.', 'usuario': UserSerializer(user).data},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'error': f'Error al crear el usuario: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )