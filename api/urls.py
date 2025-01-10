from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.ViewSets.UserViewSet import UserViewSet
from api.ViewSets.ProyectoViewSet import ProyectoViewSet
# from api.ViewSets.TallerViewSet import Taller
# from api.ViewSets.EventoView import Taller

# Definimos las rutas base de los viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'proyectos', ProyectoViewSet )

'''
    Rutas para los ViewSets de talleres y eventos
'''
# router.register(r'talleres',  TallerViewSet )
# router.register(r'eventos',  EventoViewSet )

urlpatterns = [
    path('', include(router.urls)),
]