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
    
    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Nom d\'utilisateur'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Mot de passe'),
            },
            required=['username', 'password'],
        ),
        responses={
            200: "Connexion réussie",
            404: "Identifiants invalides"
        }
    )
    # Utilisez uniquement POST pour l'authentification
    @action(detail=False, methods=['post'])
    def login(self, request):
        usernme = request.data.get('username')
        password = request.data.get('password')
        
        # Recherchez l'utilisateur par email
        user = Utilisateur.objects.filter(username=usernme, password=password).first()

        if user :
            serializer = UtilisateurSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # Si l'utilisateur n'est pas trouvé ou mot de passe incorrect
        return Response({"error": "Invalid credentials"}, status=status.HTTP_404_NOT_FOUND)
    #Documentation de l'API
    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Nom d\'utilisateur'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Mot de passe'),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='Prénom'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Nom'),
                'user_type': openapi.Schema(type=openapi.TYPE_STRING, description='Type d\'utilisateur (bailleur ou locataire)'),
                'photo_url': openapi.Schema(type=openapi.TYPE_STRING, description='URL de la photo de profil', default=''),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Adresse e-mail', default=''),
         
            },
            required=['username', 'password', 'first_name', 'last_name', 'user_type', 'photo_url', 'email'],
        ),
        responses={
            201: "Utilisateur créé avec succès",
            400: "Erreur de validation"
        }
    )
    
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        """ 
        Créer un nouvel utilisateur.
        request: requête HTTP
        return: réponse HTTP
        requuired: username, password, first_name, last_name, user_type, photo_url, email
        exemple:
        {
            "username": "
            "password": "
            "first_name": "
            "last_name": "
            "user_type": "
            "photo_url": "
            "email": "
        }
        return: {
            "response": "Utilisateur créé avec succès",
            "user": {
                "id": 1,
                "username": "user1",
                "first_name": "User",
                "last_name": "One",
                "user_type": "locataire",
                "photo_url": "",
                "email": " "
            }
            OU
            "response": "Erreur de validation",
            "errors": {
                "username": [
                    "Ce champ est obligatoire."
                ],
                "password": [
                    "Ce champ est obligatoire."
                ]
            }        
        """
        
        serializer = UtilisateurSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            message = {
                "response": "Utilisateur créé avec succès",
                "user": serializer.data
            }
            return Response(message
                            , status=status.HTTP_201_CREATED)
        message = {
            "response": "Erreur de validation",
            "errors": serializer.errors
        }
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    # Recherche d'un utilisateur par nom d'utilisateur
    @swagger_auto_schema(
        method='get',
        manual_parameters=[
            openapi.Parameter('username', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Nom d\'utilisateur', required=True),
        ],
        responses={
            200: "Utilisateur trouvé",
            404: "Utilisateur non trouvé"
        }
    ) 
    @action(detail=False, methods=['get'])
    def get_user_by_username(self, request):
        """
        Rechercher un utilisateur par nom d'utilisateur.
        request: requête HTTP
        return: réponse HTTP
        required: username
        exemple: /api/utilisateurs/get_user_by_username?username=user1
        return:
        {
            "id": 1,
            "username": "user1",
            "first_name": "User",
            "last_name": "One",
            "user_type": "locataire",
            "photo_url": "",
            "email": " "
        }
        OU
        {
            "error": "User not found"
        }
        
        """
        username = request.query_params.get('username')
        user = Utilisateur.objects.filter(username=username).first()
        if user:
            serializer = UtilisateurSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    # Recherche des utilisateurs par type
    @swagger_auto_schema(
        method='get',
        manual_parameters=[
            openapi.Parameter('user_type', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Type d\'utilisateur', required=True),
            
        ],
        responses={
            200: "Utilisateurs trouvés",
            404: "Utilisateurs non trouvés"
        }
    )
    @action(detail=False, methods=['get'])    
    def get_users_by_type(self, request):
        """
        Rechercher les utilisateurs par type.
        request: requête HTTP
        return: réponse HTTP
        required: user_type
        exemple: /api/utilisateurs/get_users_by_type?user_type=locataire
        return:
        {
            "response": "Utilisateurs trouvés",
            "users": [
            {
                "id": 1,
                "username": "user1",
                "first_name": "User",
                "last_name": "One",
                "user_type": "locataire",
                "photo_url": "",
                "email": " "
            },
            {
                "id": 2,
                "username": "user2",
                "first_name": "User",
                "last_name": "Two",
                "user_type": "locataire",
                "photo_url": "",
                "email": " "
            }
        ]}
        OU
        {   "users": [],
            "response": "Users not found"
        }
        
        """
        user_type = request.query_params.get('user_type')
        users = Utilisateur.objects.filter(user_type=user_type)
        if users:
            
            serializer = UtilisateurSerializer(users, many=True)
            message= {
                "response": "Utilisateurs trouvés",
                "users": serializer.data
            }
            return Response(message, status=status.HTTP_200_OK)
        message ={
            "response": "Users not found",
            "users": []
            
                       }
        return Response(message, status=status.HTTP_404_NOT_FOUND)



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
                openapi.IN_QUERY,
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
    
    