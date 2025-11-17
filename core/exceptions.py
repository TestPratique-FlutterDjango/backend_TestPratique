from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError as DjangoValidationError


def custom_exception_handler(exc, context):
    """
    Gestionnaire d'exceptions personnalisé pour DRF
    """
    # Appeler le gestionnaire par défaut de DRF
    response = exception_handler(exc, context)
    
    # Gérer les ValidationError de Django
    if isinstance(exc, DjangoValidationError):
        return Response({
            'error': 'Validation error',
            'details': exc.message_dict if hasattr(exc, 'message_dict') else str(exc)
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Si DRF a géré l'exception
    if response is not None:
        custom_response = {
            'error': True,
            'message': 'Une erreur est survenue',
            'details': response.data
        }
        
        # Personnaliser les messages d'erreur courants
        if response.status_code == 404:
            custom_response['message'] = 'Ressource non trouvée'
        elif response.status_code == 403:
            custom_response['message'] = 'Accès refusé'
        elif response.status_code == 401:
            custom_response['message'] = 'Authentification requise'
        elif response.status_code == 400:
            custom_response['message'] = 'Données invalides'
        elif response.status_code == 500:
            custom_response['message'] = 'Erreur interne du serveur'
        
        response.data = custom_response
    
    return response


class BusinessException(Exception):
    """Exception pour les erreurs métier"""
    def __init__(self, message, code=None):
        self.message = message
        self.code = code
        super().__init__(self.message)