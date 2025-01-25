from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.ViewSets.UserViewSet import UserViewSet
from api.ViewSets.ProyectoViewSet import ProyectoViewSet
# from api.ViewSets.TallerViewSet import Taller
# from api.ViewSets.EventoView import Taller


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'proyectos', ProyectoViewSet )

urlpatterns = [
    path('', include(router.urls)),
]