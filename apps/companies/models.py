from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel


class Company(TimeStampedModel):
    """Modèle représentant une entreprise liée à un utilisateur"""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='companies',
        verbose_name=_('utilisateur')
    )
    
    name = models.CharField(_('nom de l\'entreprise'), max_length=255)
    
    cfe_number = models.CharField(
        _('numéro CFE'),
        max_length=50,
        unique=True,
        help_text=_('Centre de Formalités des Entreprises')
    )
    
    address = models.TextField(_('adresse'))
    
    phone = models.CharField(
        _('téléphone'),
        max_length=20,
        blank=True,
        null=True
    )
    
    email = models.EmailField(
        _('email de l\'entreprise'),
        blank=True,
        null=True
    )
    
    description = models.TextField(
        _('description'),
        blank=True,
        help_text=_('Description de l\'entreprise')
    )
    
    website = models.URLField(
        _('site web'),
        blank=True,
        null=True
    )
    
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Indique si l\'entreprise est active')
    )
    
    class Meta:
        verbose_name = _('entreprise')
        verbose_name_plural = _('entreprises')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['cfe_number']),
        ]
        unique_together = [['user', 'name']]
    
    def __str__(self):
        return f"{self.name} ({self.cfe_number})"
    
    def clean(self):
        """Validation personnalisée"""
        super().clean()
        from django.core.exceptions import ValidationError
        
        # Vérifier que l'utilisateur a un compte professionnel
        if not self.user.is_professional():
            raise ValidationError({
                'user': _('Seuls les comptes professionnels peuvent ajouter des entreprises')
            })