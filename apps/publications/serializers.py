from rest_framework import serializers
from django.utils import timezone
from .models import Publication
from apps.accounts.serializers import UserSerializer
from apps.companies.serializers import CompanyListSerializer


class PublicationSerializer(serializers.ModelSerializer):
    """Serializer complet pour les publications"""
    
    author = UserSerializer(read_only=True)
    company = CompanyListSerializer(read_only=True)
    tags_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Publication
        fields = [
            'id', 'author', 'company',
            'title', 'content', 'status', 'slug',
            'image', 'views_count', 'published_at',
            'tags', 'tags_list',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'author', 'slug', 'views_count',
            'published_at', 'created_at', 'updated_at'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pas besoin de définir company_id ici car on ne l'utilise plus
    
    def get_tags_list(self, obj):
        """Retourne la liste des tags"""
        return obj.get_tags_list()
    
    def validate(self, attrs):
        """Validation des données"""
        # Vérifier que l'entreprise appartient à l'utilisateur si fournie
        company = attrs.get('company')
        if company:
            request = self.context.get('request')
            if company.user != request.user:
                raise serializers.ValidationError({
                    'company': 'Cette entreprise ne vous appartient pas'
                })
        return attrs
    
    def create(self, validated_data):
        """Crée une publication en associant l'auteur"""
        request = self.context.get('request')
        validated_data['author'] = request.user
        
        # Si le statut est publié, définir published_at
        if validated_data.get('status') == Publication.Status.PUBLISHED:
            validated_data['published_at'] = timezone.now()
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """Met à jour une publication"""
        # Si on passe de brouillon à publié, définir published_at
        if (instance.status != Publication.Status.PUBLISHED and
            validated_data.get('status') == Publication.Status.PUBLISHED):
            validated_data['published_at'] = timezone.now()
        
        return super().update(instance, validated_data)


class PublicationListSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour la liste des publications"""
    
    author_name = serializers.CharField(source='author.full_name', read_only=True)
    company_name = serializers.CharField(source='company.name', read_only=True)
    
    class Meta:
        model = Publication
        fields = [
            'id', 'title', 'author_name', 'company_name',
            'status', 'slug', 'views_count',
            'published_at', 'created_at'
        ]


class PublicationCreateSerializer(serializers.ModelSerializer):
    """Serializer pour la création d'une publication"""
    
    class Meta:
        model = Publication
        fields = [
            'title', 'content', 'company',
            'status', 'image', 'tags'
        ]
    
    def validate(self, attrs):
        """Validation des données"""
        company = attrs.get('company')
        if company:
            request = self.context.get('request')
            # Vérifier que l'entreprise appartient à l'utilisateur
            if company.user != request.user:
                raise serializers.ValidationError({
                    'company': 'Cette entreprise ne vous appartient pas'
                })
        return attrs


class PublicationUpdateSerializer(serializers.ModelSerializer):
    """Serializer pour la mise à jour d'une publication"""
    
    class Meta:
        model = Publication
        fields = [
            'title', 'content', 'company',
            'status', 'image', 'tags'
        ]
    
    def validate(self, attrs):
        """Validation des données"""
        company = attrs.get('company')
        if company:
            request = self.context.get('request')
            # Vérifier que l'entreprise appartient à l'utilisateur
            if company.user != request.user:
                raise serializers.ValidationError({
                    'company': 'Cette entreprise ne vous appartient pas'
                })
        return attrs