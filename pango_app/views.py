from django.shortcuts import render
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
#impprte decoreators
from rest_framework.decorators import action,api_view
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import *
from .serializers import *
from .filters_models import *

class UtilisateurViewSet(viewsets.ModelViewSet):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer
       
    filter_backends = [DjangoFilterBackend]
    filterset_class=UtilisateurFilter
    
    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Mot de passe'),
            },
            required=['email', 'password'],
        ),
        responses={
            200: "Connexion réussie",
            404: "Identifiants invalides"
        }
    )
    # Utilisez uniquement POST pour l'authentification
    @action(detail=False, methods=['post'])
    def login(self, request):
        usernme = request.data.get('email')
        password = request.data.get('password')
        try:
        # Recherchez l'utilisateur par email
            user = Utilisateur.objects.filter(email=usernme, password=password).first()
            serializer_user = UtilisateurSerializer(user)
            data = {
                'user': serializer_user.data
            }
            
            if user :
                
                serializer = UtilisateurSerializer(user)
                return Response(data, status=status.HTTP_200_OK)
                
            
            
        except Utilisateur.DoesNotExist:
            return Response({"message":"user not found"}, status=status.HTTP_400_BAD_REQUEST)
        except Adresse.DoesNotExist:
            print('e')
            print('e')
        
        # Si l'utilisateur n'est pas trouvé ou mot de passe incorrect
        return Response({"error": "Invalid credentials"}, status=status.HTTP_404_NOT_FOUND)
    #Documentation de l'API
   

class Mot_cleViewSet(viewsets.ModelViewSet):
    queryset = Mot_cle.objects.all()
    serializer_class = Mot_cleSerializer

class BienImmobilierViewSet(viewsets.ModelViewSet):
    queryset = BienImmobilier.objects.all()
    serializer_class = BienImmobilierSerializer    
    filter_backends = [DjangoFilterBackend]
    filterset_class=BienImmobilierFilter
class AdresseViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les adresses.
    Les adresses peuvent être filtrées par 'ville' et 'id'.
    """
    
    queryset = Adresse.objects.all()
    serializer_class = AdresseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class=AdresseFilter
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'ville',
                openapi.IN_QUERY,  # <-- Fixed!
                description="Filtrer par ville (ex: ?ville=Bukavu)",
                type=openapi.TYPE_STRING
            ),
            
            openapi.Parameter(
                'commune',
                openapi.IN_QUERY,
                description="Filtrer par commune (ex: ?commune=Ibanda)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'id',
                openapi.IN_QUERY,
                description="Filtrer par ID de l'adresse (ex: ?id=1)",
                type=openapi.TYPE_INTEGER
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        """
        Liste les adresses avec possibilité de filtrer par 'ville' et 'id'.
        Exemple d'URL de requête : /api/adresse/?ville=Kinshasa&id=1
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'ville': openapi.Schema(type=openapi.TYPE_STRING, description='Ville'),
                'commune': openapi.Schema(type=openapi.TYPE_STRING, description='Commune'),
                'quartier': openapi.Schema(type=openapi.TYPE_STRING, description='Quartier'),
                'cellule': openapi.Schema(type=openapi.TYPE_STRING, description='Cellule'),
                'avenue': openapi.Schema(type=openapi.TYPE_STRING, description='Avenue'),
                'num_av': openapi.Schema(type=openapi.TYPE_STRING, description='Numéro de l\'avenue'),
            },
            required=['ville', 'commune', 'quartier', 'cellule', 'avenue', 'num_av'],
        ),
        responses={
            201: "Adresse créée avec succès",
            400: "Erreur de validation"
        }
    )
    @action(detail=False, methods=['post'])
    def register_adresse(self, request):
        """
        Créer une nouvelle adresse.
        
        Champs requis: ville, commune, quartier, cellule, avenue, num_av.
        """
        serializer = AdresseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            message = {
                "response": "Adresse créée avec succès",
                "adresse": serializer.data
            }
            return Response(message, status=status.HTTP_201_CREATED)
        message = {
            "response": "Erreur de validation",
            "errors": serializer.errors
        }
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
        
        
class PayementViewSet(viewsets.ModelViewSet):
    queryset = Payement.objects.all()
    serializer_class = PayementSerializer
    filter_backends=[DjangoFilterBackend]
    filterset_class=PayementFilter    
class ContratLocationViewSet(viewsets.ModelViewSet):
    queryset = ContratLocation.objects.all()
    serializer_class = ContratLocationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ContratLocationFilter
   
class EvenementViewSet(viewsets.ModelViewSet):
    queryset = Evenement.objects.all()
    serializer_class = EvenementSerializer
    
    