from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView,
    create_superuser_temp,
    login_view,
    ProfileView,
    change_password_view,
    logout_view
)

app_name = 'accounts'

urlpatterns = [
    # Inscription et connexion
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    # Gestion du profil
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', change_password_view, name='change-password'),
    
    # Refresh token
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]