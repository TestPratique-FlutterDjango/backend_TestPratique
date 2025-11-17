from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Publication
from .serializers import (
    PublicationSerializer,
    PublicationListSerializer,
    PublicationCreateSerializer,
    PublicationUpdateSerializer
)
from .permissions import IsAuthorOrReadOnly
from .filters import PublicationFilter


class PublicationViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des publications
    
    list: Récupère toutes les publications publiées (publique) ou toutes les publications de l'utilisateur
    create: Crée une nouvelle publication
    retrieve: Récupère une publication spécifique
    update: Met à jour une publication
    partial_update: Met à jour partiellement une publication
    destroy: Supprime une publication
    search: Recherche de publications
    """
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PublicationFilter
    search_fields = ['title', 'content', 'tags']
    ordering_fields = ['created_at', 'published_at', 'views_count', 'title']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Retourne les publications selon l'utilisateur et l'action
        - Pour list: publications publiées OU publications de l'utilisateur
        - Pour mes-publications: toutes les publications de l'utilisateur
        """
        user = self.request.user
        
        if self.action == 'my_publications':
            # Toutes les publications de l'utilisateur
            return Publication.objects.filter(author=user).select_related('author', 'company')
        
        # Publications publiées + publications de l'utilisateur (tous statuts)
        return Publication.objects.filter(
            Q(status=Publication.Status.PUBLISHED) | Q(author=user)
        ).select_related('author', 'company').distinct()
    
    def get_serializer_class(self):
        """Retourne le serializer approprié selon l'action"""
        if self.action == 'list':
            return PublicationListSerializer
        elif self.action == 'create':
            return PublicationCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return PublicationUpdateSerializer
        return PublicationSerializer
    
    def get_permissions(self):
        """Permissions personnalisées selon l'action"""
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return super().get_permissions()
    
    def retrieve(self, request, *args, **kwargs):
        """Récupère une publication et incrémente les vues"""
        instance = self.get_object()
        
        # Incrémenter les vues seulement si ce n'est pas l'auteur
        if request.user != instance.author:
            instance.increment_views()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """Crée une nouvelle publication"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        publication = serializer.save()
        
        return Response({
            'publication': PublicationSerializer(publication, context={'request': request}).data,
            'message': 'Publication créée avec succès'
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        """Met à jour une publication"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        publication = serializer.save()
        
        return Response({
            'publication': PublicationSerializer(publication, context={'request': request}).data,
            'message': 'Publication mise à jour avec succès'
        })
    
    def destroy(self, request, *args, **kwargs):
        """Supprime une publication"""
        instance = self.get_object()
        instance.delete()
        
        return Response({
            'message': 'Publication supprimée avec succès'
        }, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    def my_publications(self, request):
        """Récupère toutes les publications de l'utilisateur connecté"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = PublicationListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = PublicationListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Recherche avancée de publications
        Paramètres: q (query), status, author, company, tags
        """
        queryset = self.get_queryset()
        
        # Recherche par texte
        query = request.query_params.get('q', None)
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__icontains=query)
            )
        
        # Filtrage par statut
        status_filter = request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filtrage par entreprise
        company_id = request.query_params.get('company', None)
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        
        # Filtrage par tags
        tags = request.query_params.get('tags', None)
        if tags:
            queryset = queryset.filter(tags__icontains=tags)
        
        # Pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PublicationListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = PublicationListSerializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """Publie une publication (change le statut en PUBLISHED)"""
        publication = self.get_object()
        
        if publication.status == Publication.Status.PUBLISHED:
            return Response({
                'error': 'Cette publication est déjà publiée'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        publication.status = Publication.Status.PUBLISHED
        from django.utils import timezone
        publication.published_at = timezone.now()
        publication.save()
        
        return Response({
            'publication': PublicationSerializer(publication, context={'request': request}).data,
            'message': 'Publication publiée avec succès'
        })
    
    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        """Archive une publication"""
        publication = self.get_object()
        publication.status = Publication.Status.ARCHIVED
        publication.save()
        
        return Response({
            'publication': PublicationSerializer(publication, context={'request': request}).data,
            'message': 'Publication archivée avec succès'
        })