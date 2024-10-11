from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UtilisateurViewSet,AdresseViewSet,ContratLocationViewSet,BienImmobilierViewSet,EvenementViewSet

# Créez un router qui gère automatiquement les routes pour le ViewSet
router = DefaultRouter()
router.register(r'utilisateurs', UtilisateurViewSet, basename='utilisateur')

router.register(r'adresse', AdresseViewSet, basename='adresse')
router.register(r'bien_imobilier', BienImmobilierViewSet, basename='bien_imobilier')

router.register(r'contrat_location',ContratLocationViewSet,basename='contrat_location')
# 
router.register(r'evenement',EvenementViewSet,basename='evenement')


#add
