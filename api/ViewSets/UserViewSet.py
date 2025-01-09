from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from ..Models.UserModel import User
from ..Serializers.UserSerializer import UserSerializer
from ..Models.ProyectoModel import Proyecto
from ..Serializers.ProyectoSerializer import ProyectoSerializer

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

    # Método para asignar a un usuario un proyecto
    @action(detail=True, methods=['post'], url_path='asignar_proyecto')
    def asignar_proyecto(self, request, pk=None):
        # Obtenemos el usuario proporcionado por el pk
        usuario = self.get_object()

        # Obtenemos los parámetros de la solicitud correctamente
        id_proyecto = request.data.get('id_proyecto', None)

        # Comprobamos que el id_proyecto no este vacío
        if not id_proyecto:
            return Response(
                {'error': 'El campo "id_proyecto" es obligatorio.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Comprobamos que el formato de el id es correcto
            id_proyecto = int(id_proyecto)

            # Obtenemos un proyecto con el id proporcionado
            proyecto = Proyecto.objects.get(id=id_proyecto)

            # Asignamos el proyecto a el usuario
            usuario.proyectos.add(proyecto)


            # Guardamos el usuario en la bbdd
            usuario.save()

            return Response(
                {'exitoso': 'Proyecto asignado correctamente.'},
                status=status.HTTP_202_ACCEPTED
            )

        except ValueError:
            return Response(
                {'error': 'El ID del proyecto debe ser un número válido.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Proyecto.DoesNotExist:
            return Response(
                {'error': 'El proyecto con el ID proporcionado no existe.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Error inesperado: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # Método para obtener todos los proyectos por usuario
    @action(detail=False, methods=['get'])
    def get_proyects_user(self, request):
        # Obtenemos el id de el usuario desde el mismo endpoint
        id_usuario = request.query_params.get('id_usuario', None)

        if not id_usuario:
            return Response(
                {'error': 'El campo "id_usuario" es obligatorio.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Validamos el formato de el id de el usuario
            id_usuario = int(id_usuario)

            # Obtenemos el usuario
            usuario = User.objects.get(id=id_usuario)

            # Obtenemos los proyectos que se asocien con el usuario
            proyectos = usuario.proyectos.all()

            serializer = ProyectoSerializer(proyectos, many=True)
            return Response({'proyectos: ':serializer.data}, status=status.HTTP_200_OK)

        # Manejo de errores específicos
        except ValueError:
            return Response(
                {'error': 'El ID del usuario debe ser un número válido.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist:
            return Response(
                {'error': 'El usuario con el ID proporcionado no existe.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Error inesperado: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
