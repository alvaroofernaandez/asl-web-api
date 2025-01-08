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

    @action(detail=True, methods=['post'], url_path='add-imagen-desde-directorio')
    def add_imagen_desde_directorio(self, request, pk=None):
        # Obtén el proyecto por su ID
        proyecto = self.get_object()

        # Aquí tomamos el nombre del archivo de la imagen como un parámetro en la solicitud
        nombre_imagen = request.data.get('nombre_imagen')

        if not nombre_imagen:
            return Response({'error': 'El nombre de la imagen es obligatorio.'}, status=status.HTTP_400_BAD_REQUEST)

        # Define la ruta completa del archivo en el directorio 'media/imagenes'
        ruta_imagen = os.path.join(settings.MEDIA_ROOT, 'imagenes', nombre_imagen)

        # Verifica si el archivo existe en el directorio
        if not os.path.exists(ruta_imagen):
            return Response({'error': 'La imagen no existe en el directorio especificado.'},
                            status=status.HTTP_404_NOT_FOUND)

        # Asigna la imagen al campo 'imagen' del proyecto
        proyecto.imagen = 'imagenes/' + nombre_imagen
        proyecto.save()

        return Response({'status': 'Imagen añadida correctamente al proyecto.'}, status=status.HTTP_200_OK)
