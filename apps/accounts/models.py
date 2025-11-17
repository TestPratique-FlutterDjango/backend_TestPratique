from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel


class UserManager(BaseUserManager):
    """Manager personnalisé pour le modèle User"""
    
    def create_user(self, email, password=None, **extra_fields):
        """Crée et sauvegarde un utilisateur standard"""
        if not email:
            raise ValueError(_('L\'email est obligatoire'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Crée et sauvegarde un superutilisateur"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser doit avoir is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser doit avoir is_superuser=True'))
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    """Modèle utilisateur personnalisé avec support compte privé/pro"""
    
    class AccountType(models.TextChoices):
        PRIVATE = 'PRIVATE', _('Compte Privé')
        PROFESSIONAL = 'PROFESSIONAL', _('Compte Professionnel')
    
    # Champs communs
    email = models.EmailField(_('email'), unique=True)
    first_name = models.CharField(_('prénom'), max_length=150)
    last_name = models.CharField(_('nom'), max_length=150)
    address = models.TextField(_('adresse'), blank=True)
    
    # Type de compte
    account_type = models.CharField(
        _('type de compte'),
        max_length=20,
        choices=AccountType.choices,
        default=AccountType.PRIVATE
    )
    
    # Champs spécifiques aux comptes professionnels
    company_name = models.CharField(
        _('nom de l\'entreprise'),
        max_length=255,
        blank=True,
        null=True
    )
    cfe_number = models.CharField(
        _('numéro CFE'),
        max_length=50,
        blank=True,
        null=True,
        help_text=_('Centre de Formalités des Entreprises')
    )
    
    # Statuts
    is_active = models.BooleanField(_('actif'), default=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    is_verified = models.BooleanField(_('vérifié'), default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        verbose_name = _('utilisateur')
        verbose_name_plural = _('utilisateurs')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['account_type']),
        ]
    
    def __str__(self):
        return self.email
    
    @property
    def full_name(self):
        """Retourne le nom complet de l'utilisateur"""
        return f"{self.first_name} {self.last_name}".strip()
    
    def is_professional(self):
        """Vérifie si l'utilisateur a un compte professionnel"""
        return self.account_type == self.AccountType.PROFESSIONAL
    
    def clean(self):
        """Validation personnalisée"""
        super().clean()
        from django.core.exceptions import ValidationError
        
        # Validation pour les comptes professionnels
        if self.is_professional():
            if not self.company_name:
                raise ValidationError({
                    'company_name': _('Le nom de l\'entreprise est obligatoire pour un compte professionnel')
                })
            if not self.cfe_number:
                raise ValidationError({
                    'cfe_number': _('Le numéro CFE est obligatoire pour un compte professionnel')
                })