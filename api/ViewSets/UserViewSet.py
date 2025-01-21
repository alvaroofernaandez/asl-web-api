from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import Token

from ..models import User
from ..Serializers.UserSerializer import UserSerializer
from ..Models.ProyectoModel import Proyecto
from ..Serializers.ProyectoSerializer import ProyectoSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Metodo para obtener usuarios ordenados tanto por cantidad como por antiguedad (de más nuevos a más antiguos)
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated]) # Esta linea permite comprobar si esta autenticado
    def get_pageable_users(self, request):
        cantidad_usuarios = request.query_params.get('cantidad', 3)  # Cantidad de usuarios por defecto es de 3
        try:
            cantidad_usuarios = int(cantidad_usuarios)
        except ValueError:
            cantidad_usuarios = 3  # Asignamos por defecto el valor de 3

        # Filtramos por los usuarios más nuevos
        usuarios_filtrados = (User.objects.all()
                                          .order_by('-antiguedad')[:cantidad_usuarios])
        serializer = UserSerializer(usuarios_filtrados, many=True)
        return Response(serializer.data)

    # Método para crear usuarios
    @action(detail=False, methods=['post'], permission_classes=[IsAdminUser])
    def create_user(self, request):
        # Recogemos los datos del cuerpo de la solicitud
        nombre = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        role = request.data.get('role', 'user')  # Asignamos el valor de 'user' si no se proporciona

        # Validamos que los campos no están vacíos
        if not all([nombre, email, password]):
            return Response({'error': 'Todos los campos (nombre, email, password) son obligatorios.'},
                        status=status.HTTP_400_BAD_REQUEST)

        try:
            # Creamos un nuevo usuario y asignamos el rol correspondiente
            user = User.objects.create(
                username=nombre,
                email=email,
                role=role,
            )

            # Usamos el método set_password para asegurar que la contraseña se guarda de manera segura
            user.set_password(password)

            # Guardamos el usuario en la base de datos
            user.save()

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
    @action(detail=False, methods=['post'], permission_classes=[IsAdminUser])
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
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
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

    # Endpoint para obtener los usuarios más recientes
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def get_pageable_first_users(self, request):
        cantidad_users = request.query_params.get('cantidad', 3)

        try:
            # Comprobamos que cantidad_users tiene el formato correcto
            cantidad_users = int(cantidad_users)
        except:
            return Response(
                {'error': 'Cantidad de users debe de ser de tipo entero'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # De el siguiente modo filtramos por la fecha de creacion de modo que obtendremos los usuarios más antiguos
        usuarios_filtrados = (User.objects
                              .all()
                              .order_by('antiguedad')[:cantidad_users])

        # Serializar los usuarios filtrados
        serializer = self.get_serializer(usuarios_filtrados, many=True)

        # Devolver los usuarios filtrados
        return Response(
            {'usuarios': serializer.data},
            status=status.HTTP_200_OK
        )

    # Funcion para obtener los usuarios que tenemos en total
    @action(detail=False, methods=['GET'])
    def obtener_cantidad_users(self, request):
        # Obtenemos los usuarios totales
        usuarios_totales = User.objects.all().count()

        # Obtenemos los usuarios con el rol de 'user'
        usuarios_normales = User.objects.filter(role='user').count()

        # Obtenemos los usuarios con el rol de 'admin'
        usuarios_administradores = User.objects.filter(role='admin').count()

        # Si deseas devolver estos valores en un diccionario como respuesta
        return Response(
            {
                'usuarios_totales': usuarios_totales,
                'usuarios_normales': usuarios_normales,
                'usuarios_administradores': usuarios_administradores
            },
            status=status.HTTP_200_OK
        )

