import os
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from config import settings
from ..Models.ProyectoModel import Proyecto
from ..Serializers.ProyectoSerializer import ProyectoSerializer

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






