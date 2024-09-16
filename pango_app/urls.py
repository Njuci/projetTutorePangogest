from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UtilisateurViewSet

# Créez un router qui gère automatiquement les routes pour le ViewSet
router = DefaultRouter()
router.register(r'utilisateurs', UtilisateurViewSet, basename='utilisateur')
