from rest_framework import permissions


class IsCompanyOwner(permissions.BasePermission):
    """
    Permission personnalisée pour vérifier que l'utilisateur
    est le propriétaire de l'entreprise
    """
    
    def has_object_permission(self, request, view, obj):
        # L'utilisateur doit être le propriétaire de l'entreprise
        return obj.user == request.user