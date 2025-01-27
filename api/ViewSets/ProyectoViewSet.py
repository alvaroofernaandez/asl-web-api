import os

from django.db.models import Count
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from config import settings
from ..Models.ProyectoModel import Proyecto
from ..Serializers.ProyectoSerializer import ProyectoSerializer
from ..permissions import IsAdminUser

class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer
    parser_classes = (MultiPartParser, FormParser)  # Esto permite manipular imágenes

    '''
        Método para añadir una imagen que tengamos en la carpeta media en la bbdd.
        Cuando ponemos detail = False, significa que vamos a tratar con un objeto por lo tanto vamos a necesitar de una
        pk que en principio es none ya que lo tenemos en los parametros de la funcion para prevenir errores
    '''

    @action(detail=True, methods=['post'], url_path='add-imagen-desde-directorio')
    def add_imagen_desde_directorio(self, request, pk=None):
        # Obtén el proyecto por su ID
        proyecto = self.get_object()

        # Obtenemos el nombre de la imagen en el cuerpo de la solicitud
        nombre_imagen = request.data.get('nombre_imagen')

        if not nombre_imagen:
            return Response({'error': 'El nombre de la imagen es obligatorio.'}, status=status.HTTP_400_BAD_REQUEST)

        # Creamos la ruta segun el directorio 'media/imagenes'
        ruta_imagen = os.path.join(settings.MEDIA_ROOT, 'imagenes', nombre_imagen)

        # Verificamos si existe el directorio
        if not os.path.exists(ruta_imagen):
            return Response({'error': 'La imagen no existe en el directorio especificado.'},
                            status=status.HTTP_404_NOT_FOUND)

        # Ahora lo que hacemos es asignar la imagen a el proyecto y guardamos el proyecto en la bbdd
        proyecto.imagen = 'imagenes/' + nombre_imagen
        proyecto.save()

        return Response({'status': 'Imagen añadida correctamente al proyecto.'}, status=status.HTTP_200_OK)

    # Funcion para crear un proyecto que esta capada para que solo los usuarios administradores puedan crear proyectos
    @action(methods=['post'], detail=False,permission_classes=[IsAdminUser])
    def create_proyect(self, request):
        # Pasamos a el serializer los datos de la request
        serializer = ProyectoSerializer(data=request.data)
        # Comprobamos mediante el metodo is_valid si los datos introducidos por el usuario son correctos
        if serializer.is_valid():
            # Guardamos el proyecto en la bbdd en caso de que sea correcto
            proyecto = serializer.save()
            return Response({'status': 'Proyecto creado correctamente.', 'proyecto': ProyectoSerializer(proyecto).data},
                            status=status.HTTP_201_CREATED)

        # Devolvemos un mensaje de error en caso de que no se guarde en la bbdd es decir no tenga el formato correcto
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Funcion para obtener los 3 últimos proyectos
    @action(methods=['get'], detail=False)
    def get_last_proyects(self, request):
        # Obtenemos los 3 últimos proyectos
        proyectos = (Proyecto
                     .objects.all()).order_by('-id')[:3]

        serializer = ProyectoSerializer(proyectos, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # Funcion para obtener los 3 primeros proyectos
    @action(methods=['get'], detail=False)
    def get_new_proyects(self, request):
        # Obtenemos los 3 últimos proyectos
        proyectos = Proyecto.objects.all().order_by('id')[:3]

        serializer = ProyectoSerializer(proyectos, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    '''
        Si hay proyectos sin participantes, los mostraremos en en este endpoint segun los que son más antiguos y luego ir
        filtrando por su capacidad.
    '''
    @action(methods=['get'],detail=False)
    def get_empty_proyects(self,request):
        proyectos = (Proyecto.objects.all()
                         .annotate(num_usuarios=Count('usuarios'))
                         .filter(num_usuarios=0)
                         .order_by('id')
                         .distinct()) # Utilizamos distinct para evitar duplicados

        serializer = ProyectoSerializer(proyectos, many=True)

        # Comprobamos si hay proyectos sin participantes
        if proyectos is None:
            return Response({'error':'No hay proyectos sin participantes'},status=status.HTTP_404_NOT_FOUND)

        return Response({'proyectos sin usuarios: ':serializer.data},status=status.HTTP_200_OK)