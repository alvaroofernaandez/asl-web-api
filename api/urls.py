from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.ViewSets.UserViewSet import UserViewSet
from api.ViewSets.ProyectoViewSet import ProyectoViewSet

# Definimos las rutas base de los viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'proyectos', ProyectoViewSet )

urlpatterns = [
    path('', include(router.urls)),
]