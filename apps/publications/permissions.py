from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée pour permettre la lecture à tous
    mais l'édition uniquement à l'auteur de la publication
    """
    
    def has_permission(self, request, view):
        # Autoriser la lecture pour tout le monde
        if request.method in permissions.SAFE_METHODS:
            return True
        # Autoriser la création uniquement aux utilisateurs authentifiés
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Autoriser la lecture pour tout le monde
        if request.method in permissions.SAFE_METHODS:
            return True
        # L'édition/suppression uniquement pour l'auteur
        return obj.author == request.user