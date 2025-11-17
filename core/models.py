from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class UUIDModel(models.Model):
    """Modèle abstrait avec UUID comme clé primaire"""
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    """Modèle abstrait avec timestamps automatiques"""
    
    created_at = models.DateTimeField(
        _('créé le'),
        auto_now_add=True
    )
    
    updated_at = models.DateTimeField(
        _('modifié le'),
        auto_now=True
    )
    
    class Meta:
        abstract = True
        ordering = ['-created_at']


class SoftDeleteModel(models.Model):
    """Modèle abstrait avec suppression douce (soft delete)"""
    
    is_deleted = models.BooleanField(
        _('supprimé'),
        default=False
    )
    
    deleted_at = models.DateTimeField(
        _('supprimé le'),
        null=True,
        blank=True
    )
    
    class Meta:
        abstract = True
    
    def soft_delete(self):
        """Effectue une suppression douce"""
        from django.utils import timezone
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
    
    def restore(self):
        """Restaure un élément supprimé"""
        self.is_deleted = False
        self.deleted_at = None
        self.save()