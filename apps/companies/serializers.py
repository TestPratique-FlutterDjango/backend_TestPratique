from rest_framework import serializers
from .models import Company
from apps.accounts.serializers import UserSerializer


class CompanySerializer(serializers.ModelSerializer):
    """Serializer pour les entreprises"""
    
    user = UserSerializer(read_only=True)
    publications_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Company
        fields = [
            'id', 'user', 'name', 'cfe_number', 'address',
            'phone', 'email', 'description', 'website',
            'is_active', 'publications_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def get_publications_count(self, obj):
        """Retourne le nombre de publications de l'entreprise"""
        return obj.publications.filter(status='PUBLISHED').count()
    
    def validate(self, attrs):
        """Validation personnalisée"""
        request = self.context.get('request')
        
        # Vérifier que l'utilisateur a un compte professionnel
        if request and not request.user.is_professional():
            raise serializers.ValidationError(
                'Seuls les comptes professionnels peuvent créer des entreprises'
            )
        
        return attrs
    
    def create(self, validated_data):
        """Crée une nouvelle entreprise en associant l'utilisateur courant"""
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


class CompanyListSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour la liste des entreprises"""
    
    publications_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Company
        fields = [
            'id', 'name', 'cfe_number', 'email',
            'is_active', 'publications_count', 'created_at'
        ]
    
    def get_publications_count(self, obj):
        """Retourne le nombre de publications de l'entreprise"""
        return obj.publications.filter(status='PUBLISHED').count()


class CompanyUpdateSerializer(serializers.ModelSerializer):
    """Serializer pour la mise à jour d'une entreprise"""
    
    class Meta:
        model = Company
        fields = [
            'name', 'address', 'phone', 'email',
            'description', 'website', 'is_active'
        ]
    
    def validate_cfe_number(self, value):
        """Empêche la modification du numéro CFE"""
        if self.instance and self.instance.cfe_number != value:
            raise serializers.ValidationError(
                'Le numéro CFE ne peut pas être modifié'
            )
        return value