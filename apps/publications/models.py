from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel


class Publication(TimeStampedModel):
    """Modèle représentant une publication"""
    
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', _('Brouillon')
        PUBLISHED = 'PUBLISHED', _('Publié')
        ARCHIVED = 'ARCHIVED', _('Archivé')
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='publications',
        verbose_name=_('auteur')
    )
    
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE,
        related_name='publications',
        verbose_name=_('entreprise'),
        null=True,
        blank=True,
        help_text=_('Entreprise associée à la publication (optionnel)')
    )
    
    title = models.CharField(_('titre'), max_length=255)
    
    content = models.TextField(_('contenu'))
    
    status = models.CharField(
        _('statut'),
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )
    
    slug = models.SlugField(
        _('slug'),
        max_length=255,
        unique=True,
        blank=True
    )
    
    image = models.ImageField(
        _('image'),
        upload_to='publications/%Y/%m/%d/',
        blank=True,
        null=True
    )
    
    views_count = models.PositiveIntegerField(
        _('nombre de vues'),
        default=0
    )
    
    published_at = models.DateTimeField(
        _('date de publication'),
        null=True,
        blank=True
    )
    
    tags = models.CharField(
        _('tags'),
        max_length=255,
        blank=True,
        help_text=_('Tags séparés par des virgules')
    )
    
    class Meta:
        verbose_name = _('publication')
        verbose_name_plural = _('publications')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['author', 'status']),
            models.Index(fields=['company']),
            models.Index(fields=['status', '-published_at']),
            models.Index(fields=['slug']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """Génère automatiquement le slug si non fourni"""
        if not self.slug:
            from django.utils.text import slugify
            import uuid
            self.slug = f"{slugify(self.title)}-{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)
    
    def increment_views(self):
        """Incrémente le compteur de vues"""
        self.views_count += 1
        self.save(update_fields=['views_count'])
    
    @property
    def is_published(self):
        """Vérifie si la publication est publiée"""
        return self.status == self.Status.PUBLISHED
    
    def get_tags_list(self):
        """Retourne la liste des tags"""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]