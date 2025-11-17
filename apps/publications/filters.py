import django_filters
from .models import Publication


class PublicationFilter(django_filters.FilterSet):
    """Filtre pour les publications avec recherche avancée"""
    
    # Filtrage par titre (contient)
    title = django_filters.CharFilter(lookup_expr='icontains')
    
    # Filtrage par contenu (contient)
    content = django_filters.CharFilter(lookup_expr='icontains')
    
    # Filtrage par statut
    status = django_filters.ChoiceFilter(choices=Publication.Status.choices)
    
    # Filtrage par auteur
    author = django_filters.NumberFilter(field_name='author__id')
    author_email = django_filters.CharFilter(field_name='author__email', lookup_expr='icontains')
    
    # Filtrage par entreprise
    company = django_filters.NumberFilter(field_name='company__id')
    company_name = django_filters.CharFilter(field_name='company__name', lookup_expr='icontains')
    
    # Filtrage par tags
    tags = django_filters.CharFilter(lookup_expr='icontains')
    
    # Filtrage par date de création
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    
    # Filtrage par date de publication
    published_after = django_filters.DateTimeFilter(field_name='published_at', lookup_expr='gte')
    published_before = django_filters.DateTimeFilter(field_name='published_at', lookup_expr='lte')
    
    # Filtrage par nombre de vues
    min_views = django_filters.NumberFilter(field_name='views_count', lookup_expr='gte')
    max_views = django_filters.NumberFilter(field_name='views_count', lookup_expr='lte')
    
    class Meta:
        model = Publication
        fields = [
            'title', 'content', 'status', 'author', 'author_email',
            'company', 'company_name', 'tags',
            'created_after', 'created_before',
            'published_after', 'published_before',
            'min_views', 'max_views'
        ]