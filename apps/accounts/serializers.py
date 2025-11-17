from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer pour l'inscription d'un utilisateur"""
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'address', 'account_type',
            'company_name', 'cfe_number'
        ]
        read_only_fields = ['id']
    
    def validate(self, attrs):
        """Validation des données"""
        # Vérifier que les mots de passe correspondent
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                'password': 'Les mots de passe ne correspondent pas'
            })
        
        # Validation spécifique pour compte professionnel
        if attrs.get('account_type') == User.AccountType.PROFESSIONAL:
            if not attrs.get('company_name'):
                raise serializers.ValidationError({
                    'company_name': 'Le nom de l\'entreprise est obligatoire pour un compte professionnel'
                })
            if not attrs.get('cfe_number'):
                raise serializers.ValidationError({
                    'cfe_number': 'Le numéro CFE est obligatoire pour un compte professionnel'
                })
        
        return attrs
    
    def create(self, validated_data):
        """Crée un nouvel utilisateur"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    """Serializer pour afficher les informations utilisateur"""
    
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'address', 'account_type', 'company_name', 'cfe_number',
            'is_verified', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'email', 'is_verified', 'created_at', 'updated_at'
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer pour la mise à jour du profil utilisateur"""
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'address',
            'company_name', 'cfe_number'
        ]
    
    def validate(self, attrs):
        """Validation lors de la mise à jour"""
        user = self.instance
        
        # Si l'utilisateur est pro, vérifier les champs obligatoires
        if user.is_professional():
            if 'company_name' in attrs and not attrs['company_name']:
                raise serializers.ValidationError({
                    'company_name': 'Le nom de l\'entreprise ne peut pas être vide'
                })
            if 'cfe_number' in attrs and not attrs['cfe_number']:
                raise serializers.ValidationError({
                    'cfe_number': 'Le numéro CFE ne peut pas être vide'
                })
        
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer pour le changement de mot de passe"""
    
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password]
    )
    new_password_confirm = serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
        """Validation des mots de passe"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password': 'Les nouveaux mots de passe ne correspondent pas'
            })
        return attrs
    
    def validate_old_password(self, value):
        """Vérifie l'ancien mot de passe"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('L\'ancien mot de passe est incorrect')
        return value