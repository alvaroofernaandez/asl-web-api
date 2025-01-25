from rest_framework.permissions import BasePermission

class IsNormalUser(BasePermission):

    def has_permission(self, request, view):
        # Verificamos si el usuario está autenticado

        if not request.user or not request.auth:
            return False

        # Obtenemos el contenido de el token
        token_data = request.auth

        # Comprobamos si el usuario esta autenticado
        if token_data.get('role') == 'user' or token_data.get('role') == 'admin':
            return True

        return False

class IsAdminUser(BasePermission):

    def has_permission(self, request, view):
        # Verificamos si el usuario está autenticado

        if not request.user or not request.auth:
            return False

        # Obtenemos el contenido de el token
        token_data = request.auth

        # Comprobamos si el usuario esta autenticado como admin
        if token_data.get('role') == 'admin':
            return True

        return False
