from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (UtilisateurViewSet,AdresseViewSet,
                    ContratLocationViewSet,BienImmobilierViewSet,EvenementViewSet,NotificationViewSet,delete_all_notification)

# Créez un router qui gère automatiquement les routes pour le ViewSet
router = DefaultRouter()
router.register(r'utilisateurs', UtilisateurViewSet, basename='utilisateur')

router.register(r'adresse', AdresseViewSet, basename='adresse')
router.register(r'bien_imobilier', BienImmobilierViewSet, basename='bien_imobilier')

router.register(r'contrat_location',ContratLocationViewSet,basename='contrat_location')
# 
router.register(r'evenement',EvenementViewSet,basename='evenement')

#route des notifications
router.register(r'notification',NotificationViewSet,basename='notification')
#router.register(r'delete_all_notification',delete_all_notification,basename='delete_all_notification')

urlpatterns = [
    path('', include(router.urls)),
]


#add
