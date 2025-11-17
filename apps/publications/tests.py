from django.test import TestCase
from apps.accounts.models import User
from apps.publications.models import Publication


class PublicationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='author@example.com',
            password='testpass123',
            first_name='Author',
            last_name='Test'
        )
        self.publication = Publication.objects.create(
            author=self.user,
            title='Test Publication',
            content='Test content',
            status=Publication.Status.DRAFT
        )
    
    def test_publication_creation(self):
        self.assertEqual(self.publication.title, 'Test Publication')
        self.assertEqual(self.publication.author, self.user)
        self.assertFalse(self.publication.is_published)
    
    def test_slug_generation(self):
        self.assertTrue(self.publication.slug.startswith('test-publication'))