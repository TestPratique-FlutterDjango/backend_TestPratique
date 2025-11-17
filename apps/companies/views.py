from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Company
from .serializers import (
    CompanySerializer,
    CompanyListSerializer,
    CompanyUpdateSerializer
)
from .permissions import IsCompanyOwner


class CompanyViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des entreprises
    
    list: Récupère toutes les entreprises de l'utilisateur
    create: Crée une nouvelle entreprise
    retrieve: Récupère une entreprise spécifique
    update: Met à jour une entreprise
    partial_update: Met à jour partiellement une entreprise
    destroy: Supprime une entreprise
    """
    permission_classes = [IsAuthenticated, IsCompanyOwner]
    
    def get_queryset(self):
        """Retourne uniquement les entreprises de l'utilisateur connecté"""
        return Company.objects.filter(user=self.request.user).select_related('user')
    
    def get_serializer_class(self):
        """Retourne le serializer approprié selon l'action"""
        if self.action == 'list':
            return CompanyListSerializer
        elif self.action in ['update', 'partial_update']:
            return CompanyUpdateSerializer
        return CompanySerializer
    
    def create(self, request, *args, **kwargs):
        """Crée une nouvelle entreprise"""
        # Vérifier que l'utilisateur a un compte professionnel
        if not request.user.is_professional():
            return Response({
                'error': 'Seuls les comptes professionnels peuvent créer des entreprises'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company = serializer.save()
        
        return Response({
            'company': CompanySerializer(company).data,
            'message': 'Entreprise créée avec succès'
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        """Met à jour une entreprise"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        company = serializer.save()
        
        return Response({
            'company': CompanySerializer(company).data,
            'message': 'Entreprise mise à jour avec succès'
        })
    
    def destroy(self, request, *args, **kwargs):
        """Supprime une entreprise"""
        instance = self.get_object()
        
        # Vérifier s'il y a des publications liées
        publications_count = instance.publications.count()
        if publications_count > 0:
            return Response({
                'error': f'Impossible de supprimer cette entreprise car elle a {publications_count} publication(s) associée(s)'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        instance.delete()
        return Response({
            'message': 'Entreprise supprimée avec succès'
        }, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        """Active/Désactive une entreprise"""
        company = self.get_object()
        company.is_active = not company.is_active
        company.save()
        
        status_text = 'activée' if company.is_active else 'désactivée'
        
        return Response({
            'company': CompanySerializer(company).data,
            'message': f'Entreprise {status_text} avec succès'
        })
    
    @action(detail=True, methods=['get'])
    def publications(self, request, pk=None):
        """Récupère toutes les publications d'une entreprise"""
        company = self.get_object()
        publications = company.publications.all()
        
        from apps.publications.serializers import PublicationListSerializer
        serializer = PublicationListSerializer(publications, many=True)
        
        return Response({
            'count': publications.count(),
            'publications': serializer.data
        })