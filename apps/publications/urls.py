from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PublicationViewSet

app_name = 'publications'

router = DefaultRouter()
router.register(r'', PublicationViewSet, basename='publication')

urlpatterns = [
    path('', include(router.urls)),
]