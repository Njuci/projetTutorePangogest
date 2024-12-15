from .sendingemail import envoyer_email
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

from dateutil.relativedelta import relativedelta
from datetime import datetime
from django.db.models import Q
import uuid
import base64

from rest_framework import status
from rest_framework.response import Response








def recuperer_contrat_bailleur(bailleur_id):
    try:
        # Recherche des contrats liés au bailleur via le champ `bien.utilisateur_id`
        contrats = ContratLocation.objects.filter(bien__utilisateur_id=bailleur_id)
        if not contrats.exists():
            return Response({"detail": "Aucun contrat trouvé."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Préparation des données pour chaque contrat
        contrats_data = []
        for contrat in contrats:
            if contrat.locataire==None:
                locataire_info={"Contrat":"Contrat en attente d'approbation"}
            else:
                locataire_info = {
                    "id": contrat.locataire.id,
                    "first_name": contrat.locataire.first_name,
                    "last_name": contrat.locataire.last_name,
                    "email": contrat.locataire.email,
                    "telephone": contrat.locataire.telephone
                }    
            #infos sur le bien et l'adresse
            bien_info = {
                "id": contrat.bien.id,
                "surface": contrat.bien.surface,
                "photo_url": contrat.bien.photo_url,
                "description": contrat.bien.description,
                "prix": contrat.bien.prix,
                "adresse": {
                    "id": contrat.bien.adresse.id,
                    "ville": contrat.bien.adresse.ville,
                    "commune": contrat.bien.adresse.commune,
                    "quartier": contrat.bien.adresse.quartier,
                    "cellule": contrat.bien.adresse.cellule,
                    "avenue": contrat.bien.adresse.avenue,
                    "num_av": contrat.bien.adresse.num_av,
                }   
            } 
             
             
              
            contrat_data = {
                "id": contrat.id,
                "date_debut": contrat.date_debut,
                "dure": contrat.duree_mois,
                "prix": contrat.prix,
                "bien": contrat.bien.id,
                "fichier": contrat.fichier,
                "locataire": locataire_info,
                "date_contrat": contrat.date_contrat,
                "encours": contrat.encours,
                "bien_info": bien_info
                
                        }
            contrats_data.append(contrat_data)
        
        return Response(contrats_data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"detail": f"Erreur: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
 
def recuperer_contrat_locataire(locataire_id):
            try:
                # Recherche des contrats liés au locataire
                
                contrats = ContratLocation.objects.filter(locataire_id=locataire_id)
                if not contrats.exists():
                    return Response({"detail": "Aucun contrat trouvé."}, status=status.HTTP_400_BAD_REQUEST)
                
                # Préparation des données pour chaque contrat
                contrats_data = []
                for contrat in contrats:
                    bailleur_info = {
                        "id": contrat.bien.utilisateur.id,
                        "first_name": contrat.bien.utilisateur.first_name,
                        "last_name": contrat.bien.utilisateur.last_name,
                        "email": contrat.bien.utilisateur.email,
                        "telephone": contrat.bien.utilisateur.telephone
                    }
                    
                    bien_info = {
                "id": contrat.bien.id,
                "surface": contrat.bien.surface,
                "photo_url": contrat.bien.photo_url,
                "description": contrat.bien.description,
                "prix": contrat.bien.prix,
                "adresse": {
                    "id": contrat.bien.adresse.id,
                    "ville": contrat.bien.adresse.ville,
                    "commune": contrat.bien.adresse.commune,
                    "quartier": contrat.bien.adresse.quartier,
                    "cellule": contrat.bien.adresse.cellule,
                    "avenue": contrat.bien.adresse.avenue,
                    "num_av": contrat.bien.adresse.num_av,
                }   
                    } 
                    contrat_data = {
                        "id": contrat.id,
                        "date_debut": contrat.date_debut,
                        "dure": contrat.duree_mois,
                        "prix": contrat.prix,
                        "bien": contrat.bien.id,
                        "bailleur": bailleur_info,
                        "fichier": contrat.fichier,
                        "date_contrat": contrat.date_contrat,
                        "encours": contrat.encours,
                        'bien_info':bien_info
                    }
                    contrats_data.append(contrat_data)
                
                return Response(contrats_data, status=status.HTTP_200_OK)
            
            except Exception as e:
                return Response({"detail": f"Erreur: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   

def recuperer_locataires(bailleur_id):
    # Récupérer les contrats de location pour le bailleur donné
    locataires = ContratLocation.objects.filter(bien__utilisateur__id=bailleur_id).select_related('locataire')
    
    if locataires.exists():
        # Filtrer les locataires qui ne sont pas None
        locataires_list = [contrat.locataire for contrat in locataires if contrat.locataire is not None]
        
        if locataires_list:
            # Sérialiser les locataires
            serializer = UtilisateurSerializer(locataires_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Aucun locataire trouvé."}, status=status.HTTP_404_NOT_FOUND)
    
    return Response({"detail": "Aucun locataire trouvé."}, status=status.HTTP_404_NOT_FOUND)


def recuperer_bailleur(locataire_id):
    # Récupérer les contrats de location liés au locataire
    bailleurs = ContratLocation.objects.filter(locataire__id=locataire_id).select_related('bien__utilisateur')
    if bailleurs.exists():
        # Récupérer les objets 'bien'
        biens = [contrat.bien.utilisateur for contrat in bailleurs]
        
        # Sérialiser les objets bailleurs
        serializer = UtilisateurSerializer(biens, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "Aucun bailleur trouvé."}, status=status.HTTP_400_BAD_REQUEST)
    
def recuperer_maison_locataire(locataire_id):
    # Récupérer le contrat de location lié au locataire
    maison = ContratLocation.objects.filter(locataire__id=locataire_id).select_related('bien')
    
    if maison.exists():
        # Récupérer les objets 'bien'
        biens = [contrat.bien for contrat in maison]
        
        # Sérialiser les objets biens immobiliers
        serializer = BienImmobilierSerializer(biens, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response({"detail": "Aucune maison trouvée."}, status=status.HTTP_404_NOT_FOUND)

def recuperer_maisons_bailleur(bailleur_id):
    # Récupérer les contrats de location liés au bailleur
    maisons = ContratLocation.objects.filter(bien__utilisateur__id=bailleur_id).select_related('bien')
    
    if maisons.exists():
        # Récupérer les objets 'bien'
        biens = [contrat.bien for contrat in maisons]
        
        # Sérialiser les objets biens immobiliers
        serializer = BienImmobilierSerializer(biens, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response({"detail": "Aucune maison trouvée pour ce bailleur."}, status=status.HTTP_404_NOT_FOUND)


def generer_mot_cle_unique():
    uuid_bytes = uuid.uuid4().bytes  # UUID sous forme de bytes
    base64_uuid = base64.urlsafe_b64encode(uuid_bytes).decode('utf-8')  # Encodé en base64 et converti en chaîne
    return str(base64_uuid[:10])  # Tronqué à 10 caractères et converti en chaîne



def verifier_contrat_chevauchement(bien, date_debut_str, duree_mois):
    """
    Vérifie s'il existe un contrat pour le bien donné pendant la période spécifiée.

    :param bien: Instance du bien immobilier à vérifier
    :param date_debut_str: Date de début de la période sous forme de chaîne (format 'YYYY-MM-DD')
    :param date_fin_str: Date de fin de la période sous forme de chaîne (format 'YYYY-MM-DD')
    :return: True s'il existe un contrat chevauchant la période, sinon False
    """
    # Convertir les dates de chaîne en objets datetime
    date_debut = datetime.strptime(date_debut_str, "%Y-%m-%d").date()
    # Calculer la date de fin en fonction de la durée (duree_mois)
    date_fin = date_debut + relativedelta(months=int(duree_mois))
    # Calculer les contrats dont les dates chevauchent la période donnée
    contrats_chevauchants = ContratLocation.objects.filter(
        bien=bien
    ).filter(
        Q(date_debut__lte=date_fin) &  # Le contrat commence avant ou pendant la période
        Q(date_debut__gte=date_debut) |  # Le contrat commence après ou pendant la période
        Q(date_debut__lte=date_debut, # Si le contrat commence avant le début de la période
          date_debut__gte=date_fin)  # et il se termine après ou pendant la période
    )

    return contrats_chevauchants.exists()


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
                'user_type': openapi.Schema(type=openapi.TYPE_STRING, description='Type d Utilisateur'),
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
        user_type=request.data.get('user_type')
        try:
        # Recherchez l'utilisateur par email
            user = Utilisateur.objects.get(email=usernme,user_type=user_type)
            serializer_user = UtilisateurSerializer(user)
        
            if serializer_user.data['password'] == password:
                
                data = serializer_user.data
               
            
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({"message":"Mot de passe invalide"}, status=status.HTTP_401_UNAUTHORIZED)    
            
            
        except Utilisateur.DoesNotExist:
            return Response({"message":"user not found"}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['post'])
    def register(self, request):
        """
!        Créer un nouvel utilisateur.
        
        Champs requis: email, password, nom, prenom, telephone, adresse.
        """
        serializer = UtilisateurSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            message = {
                "response": "Utilisateur créé avec succès",
                "utilisateur": serializer.data
            }
            return Response(message, status=status.HTTP_201_CREATED)
        # En cas d'erreur de validation
        
        #SI L'UTILISATEUR EXISTE DEJA
        if Utilisateur.objects.filter(email=request.data['email']).exists():
            # Retourner un message d'erreur et l'instance de l'utilisateur
            
            return Response({"message":"Cet utilisateur existe déjà"}, status=status.HTTP_400_BAD_REQUEST)
        
        message = {
            "response": "Erreur de validation",
            "errors": serializer.errors
        }
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
        
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
        ²
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
    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'bien': openapi.Schema(type=openapi.TYPE_INTEGER, description='Bien'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email du locataire'),
                'date_debut': openapi.Schema(type=openapi.TYPE_STRING, description='Date du début de Contrat'),
                'date_contrat': openapi.Schema(type=openapi.TYPE_STRING, description='Date à laquelle le Contrat a été signée'),
                
                
                'duree_mois': openapi.Schema(type=openapi.TYPE_INTEGER, description='Durée du contrat en mois'),
                'fichier': openapi.Schema(type=openapi.TYPE_STRING, description='Fichier du contrat'),
                'prix': openapi.Schema(type=openapi.TYPE_STRING, description='Prix convenu pour le contrat'),
                'encours': openapi.Schema(type=openapi.TYPE_STRING, description='Statut du contrat'),
            },
            required=['bien', 'email', 'date_debut', 'duree_mois', 'prix'],
        ),
        responses={
            201: "Contrat créé avec succès",
            400: "Erreur de validation"
        }
    )
    @action(detail=False, methods=['post'])
    def register_contrat(self, request):
        """
        Créer un contrat
        Champs requis: bien, email, date_debut, duree_mois, prix
        """
        # Récupérer les données de la requête
        bien = request.data.get('bien')
        date_debut = request.data.get('date_debut')
        duree_mois = request.data.get('duree_mois')
        email = request.data.get('email')
        
        # Vérifier si le bien immobilier existe
        try:
            bien_immobilier = BienImmobilier.objects.get(id=bien)
            # Vérifier si le contrat chevauche un autre contrat
            if verifier_contrat_chevauchement(bien_immobilier, date_debut, duree_mois):
                return Response({"message": "Le contrat chevauche un autre contrat existant"}, status=status.HTTP_400_BAD_REQUEST)
        except BienImmobilier.DoesNotExist:
            return Response({"message": "Bien immobilier non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ContratLocationSerializer(data=request.data)
        # Chercher le propriétaire du bien
        proprietaire = f'{bien_immobilier.utilisateur.first_name} {bien_immobilier.utilisateur.last_name}'
        
        if serializer.is_valid():
            serializer.save()
            
            # Envoi d'un email
            contrat = serializer.data
            # Générer un mot clé
            mot_cle = generer_mot_cle_unique()
            # Enregistrer le mot clé via son serializer
            mot_cle_serializer = Mot_cleSerializer(data={'email': email, 'contrat': serializer.data['id'], 'mot_cle': mot_cle})
            if mot_cle_serializer.is_valid():
                mot_cle_serializer.save()
                
            else:
                return Response({"message": "Erreur lors de la création du mot-clé", "error": mot_cle_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
            contrat2 = {}
            # Mettre les clés en majuscule en éliminant les underscores
            for key in contrat:
                new_key = key.replace('_', ' ').upper()
                contrat2[new_key] = contrat[key]
            contrat = contrat2
            has_send = envoyer_email(email, proprietaire, contrat, mot_cle)
            if has_send:
                message = {
                    "response": "Contrat créé avec succès",
                    "contrat": serializer.data
                }
                return Response(message, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Erreur lors de l'envoi de l'email"}, status=status.HTTP_400_BAD_REQUEST)
        
        message = {
            "response": "Erreur de validation",
            "errors": serializer.errors
        }
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'mot_cle': openapi.Schema(type=openapi.TYPE_STRING, description='Mot_clé'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email du locataire'),
                },
                
            required=['mot_cle','email'],
        ),
        ) 
    @action(detail=False, methods=['post'])
    def verifier_mot_cle(self, request):
        """
        Vérifier si un mot clé et un email sont liés à un contrat
        """
        # Récupérer le mot clé et l'email dans le corps de la requête
        mot_cle = request.data.get('mot_cle')
        email = request.data.get('email')
        
        if not mot_cle or not email:
            return Response({"message": "Mot clé et email sont requis"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Rechercher le mot clé et vérifier l'email associé
            mot_cle_instance = Mot_cle.objects.get(mot_cle=mot_cle, email=email)
            contrat = mot_cle_instance.contrat
            contrat_serializer = ContratLocationSerializer(contrat)
            
            return Response(
               
                contrat_serializer.data
            , status=status.HTTP_200_OK)
        except Mot_cle.DoesNotExist:
            return Response({"message": "Mot clé ou email non trouvés ou non valides"},
                            status=status.HTTP_404_NOT_FOUND)
    
    
    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'mot_cle': openapi.Schema(type=openapi.TYPE_STRING, description='Mot_clé'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email du locataire'),
                'response': openapi.Schema(type=openapi.TYPE_STRING, description='Réponse du locataire "Accepter ou Refuser"'),},
                
            required=['mot_cle','email','response'],
        ),
        )
    
    @action(detail=False, methods=['post'])
    def validation_contrat(self, request):
        """
        Vérifier si un mot clé et un email sont liés à un contrat
        """
        # Récupérer le mot clé, l'email et la réponse dans le corps de la requête
        mot_cle = request.data.get('mot_cle')
        email = request.data.get('email')
        reponse = request.data.get('response')  # le locataire accepte ou rejette le contrat

        if not mot_cle or not email or reponse is None:
            return Response({"message": "Mot clé, email et réponse sont requis"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Rechercher le mot clé et vérifier l'email associé
            mot_cle_instance = Mot_cle.objects.get(mot_cle=mot_cle, email=email)

            # Chercher l'utilisateur associé à l'email
            user = Utilisateur.objects.get(email=email,user_type='locataire')
            if user.user_type != 'locataire':
                return Response({"errors": "Un utilisateur doit être du type locataire"}, status=status.HTTP_400_BAD_REQUEST)

            # Vérifier si le contrat a déjà un locataire
            contrat = mot_cle_instance.contrat
            if contrat.locataire is not None:
                return Response({"message": "Ce contrat a déjà un locataire"}, status=status.HTTP_400_BAD_REQUEST)

            # Gérer la réponse du locataire
            if reponse.lower() == 'accepter':
                # Assigner le locataire au contrat
                contrat.locataire = user
                contrat.save()
                contrat_serializer = ContratLocationSerializer(contrat)

                return Response(contrat_serializer.data, 
                                status=status.HTTP_200_OK)
            elif reponse.lower() == 'rejeter':
                return Response({"message": "Contrat rejeté par le locataire"}, status=status.HTTP_400_BAD_REQUEST)
            else:   
                return Response({"message": "Réponse non valide, veuillez répondre par 'accepter' ou 'rejeter'"}, 
                                status=status.HTTP_400_BAD_REQUEST)

        except Mot_cle.DoesNotExist:
            return Response({"message": "Mot clé ou email non trouvés ou non valides"}, 
                            status=status.HTTP_400_BAD_REQUEST)
        except Utilisateur.DoesNotExist:
            return Response({"message": "Aucun utilisateur associé à cet email"}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'bailleur_id': openapi.Schema(type=openapi.TYPE_STRING, description='bailleur_id')},
            required=['bailleur_id'],
        ),
        )
    
    @action(detail=False, methods=['post'])
    def locataires_par_bailleur(self, request):
        """
        Récupère les locataires associés à un bailleur spécifique.
        Cette méthode extrait l'identifiant du bailleur à partir de la requête et 
        renvoie les locataires associés à ce bailleur. Si l'identifiant du bailleur 
        n'est pas fourni, une réponse avec un message d'erreur et un statut HTTP 400 
        est renvoyée.
        Args:
            request (Request): La requête HTTP contenant les données nécessaires.
        {"bailleur_id":1}
        Returns:
            Response code 200
            [
                    {
                        "id": 2,
                        "password": "12345678",
                        "last_login": null,
                        "is_superuser": false,
                        "username": "glosingson23@gmail.com",
                        "first_name": "G-Losingson",
                        "last_name": "Birungi",
                        "email": "glosingson23@gmail.com",
                        "is_staff": false,
                        "is_active": true,
                        "date_joined": "2024-10-21T20:46:45.726487Z",
                        "photo_url": "https://firebasestorage.googleapis.com/v0/b/pangogest.appspot.com/o/profil.png?alt=media&token=800f4279-9fb1-463f-8add-c0f485310caa",
                        "user_type": "locataire",
                        "telephone": "+243813445417",
                        "id_adresse": null,
                        "groups": [],
                        "user_permissions": []
                    }d
                    ]
        Response code 400
                    {
           "detail": "Aucun locataire trouvé."
           }
        

                
                            """
        
        #documenre
        
        
        bailleur_id = request.data.get('bailleur_id')
        if not bailleur_id:
            return Response({"detail": "bailleur_id est requis."}, status=status.HTTP_400_BAD_REQUEST)
        
        return recuperer_locataires(bailleur_id)
    
    @action(detail=False, methods=['post'])
    def bailleur_par_locataire(self, request):
        """
        request: {"locataire_id":2}
        reponse : 200
                    [
                            {
                                "id": 1,
                                "password": "00000000",
                                "last_login": null,
                                "is_superuser": false,
                                "username": "georgesbyona@gmail.com",
                                "first_name": "Georges",
                                "last_name": "Byona",
                                "email": "georgesbyona@gmail.com",
                                "is_staff": false,
                                "is_active": true,
                                "date_joined": "2024-10-20T13:07:08.110676Z",
                                "photo_url": "https://lh3.googleusercontent.com/a/ACg8ocLrFO4QlXqP0Elvw0cspu9YMHbut7Os8iSPpfxtzo6NTJZtw5s=s96-c",
                                "user_type": "bailleur",
                                "telephone": "+243844300329",
                                "id_adresse": null,
                                "groups": [],
                                "user_permissions": []
                            }
                            ]
                400:
                    {
                        "detail": "Aucun bailleur trouvé."}                                    
        
        """
        
        
        locataire_id = request.data.get('locataire_id')
        if not locataire_id:
            return Response({"detail": "locataire_id est requis."}, status=status.HTTP_400_BAD_REQUEST)
        
        return recuperer_bailleur(locataire_id)
    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'locataire_id': openapi.Schema(type=openapi.TYPE_STRING, description='bailleur_id')},
            required=['locataire_id'],
        ),
        )
    
    @action(detail=False, methods=['post'])
    def maison_par_locataire(self, request):
        """
        request: {"locataire_id":2}
        response 200
                [
                    {
                        "id": 1,
                        "surface": "25x20",
                        "photo_url": "https://firebasestorage.googleapis.com/v0/b/pangogest.appspot.com/o/demo-houses%2F03.jpg?alt=media&token=e52bee36-2bcc-4e16-b0a8-c23c07703344",
                        "description": "blablabla",
                        "prix": "100.00",
                        "adresse": 1,
                        "utilisateur": 1
                    }
                    ]
        response 400:
                {
             "detail": "Aucune maison trouvée."
                }
                
                                
        
        """
        locataire_id = request.data.get('locataire_id')
        if not locataire_id:
            return Response({"detail": "locataire_id est requis."}, status=status.HTTP_400_BAD_REQUEST)
        
        return recuperer_maison_locataire(locataire_id)
    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'bailleur_id': openapi.Schema(type=openapi.TYPE_STRING, description='bailleur_id')},
            required=['bailleur_id'],
        ),
        )
    
    @action(detail=False, methods=['post'])
    def maisons_par_bailleur(self, request):
        """
            request:  {"bailleur_id":1}
       
            response 200:
            [
                        {
                            "id": 1,
                            "surface": "25x20",
                            "photo_url": "https://firebasestorage.googleapis.com/v0/b/pangogest.appspot.com/o/demo-houses%2F03.jpg?alt=media&token=e52bee36-2bcc-4e16-b0a8-c23c07703344",
                            "description": "blablabla",
                            "prix": "100.00",
                            "adresse": 1,
                            "utilisateur": 1
                        },
                        {
                            "id": 4,
                            "surface": "25x50",
                            "photo_url": "https://firebasestorage.googleapis.com/v0/b/pangogest.appspot.com/o/houses%2F1729444895680?alt=media&token=932aff43-9120-4c39-9956-5cd5229958ed",
                            "description": "Maison simple et paisible, avec 3 chambres, 3 toilettes, 1 salon et 1 cuisine.",
                            "prix": "250.00",
                            "adresse": 4,
                            "utilisateur": 1
                        }
                        ]
                                    
            
        """
        
        bailleur_id = request.data.get('bailleur_id')
        if not bailleur_id:
            return Response({"detail": "bailleur_id est requis."}, status=status.HTTP_400_BAD_REQUEST)
        
        return recuperer_maisons_bailleur(bailleur_id)
    
    
    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'bailleur_id': openapi.Schema(type=openapi.TYPE_STRING, description='bailleur_id')},
            required=['bailleur_id'],
        ),
        )
    
    
    @action(detail=False, methods=['post'])
    def contrat_par_bailleur(self, request):
        """
        Récupère les contrats associés à un bailleur spécifique.
        Cette méthode extrait l'identifiant du bailleur à partir de la requête 
        et renvoie les contrats associés à ce bailleur. 
        Si l'identifiant du bailleur n'est pas fourni, une réponse avec un message d'erreur et un statut HTTP 400 est renvoyée.

        Args:
            request (Request): La requête HTTP contenant les données nécessaires.
            {"bailleur_id":1}
        
        Returns:
            Response code 200:
                [
                    {
                        "id": 1,
                        "date_debut": "2024-01-01",
                        "date_fin": "2024-12-31",
                        "prix": "500.00",
                        "bien": 1,
                        "locataire": 2,
                        "fichier": "url_du_fichier",
                        "date_contrat": "2024-01-01",
                        "encours": true
                    },
                    ...
                ]
            
            Response code 400:
                {
                    "detail": "Aucun contrat trouvé."
                }
        """
        
        bailleur_id = request.data.get('bailleur_id')
        if not bailleur_id:
            return Response({"detail": "bailleur_id est requis."}, status=status.HTTP_400_BAD_REQUEST)
        
        return recuperer_contrat_bailleur(bailleur_id)
    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'locataire_id': openapi.Schema(type=openapi.TYPE_STRING, description='locataire_id')},
            required=['locataire_id'],
        ),
        )
    @action(detail=False,methods=['post'])
    def contrat_par_locataire(self,request):
        locataire_id = request.data.get('locataire_id')
        if not locataire_id:
            return Response({"detail": "locataire_id est requis."}, status=status.HTTP_400_BAD_REQUEST)

        return recuperer_contrat_locataire(locataire_id)
    
            
        
        
    
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = NotificationFilter
    
    #register notification
    """   utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    vu = models.BooleanField(default=False) """
    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'utilisateur': openapi.Schema(type=openapi.TYPE_INTEGER, description='Utilisateur'),
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='Message'),
                'vu': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Vu'),
            },
            required=['utilisateur', 'message'],
        ),
        responses={
            201: "Notification créée avec succès",
            400: "Erreur de validation"
        }
    )
    
    @action(detail=False, methods=['post'])
    def register_notification(self, request):
        """
        Créer une nouvelle notification.
        
        Champs requis: utilisateur, message.
        """
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            message = {
                "response": "Notification créée avec succès",
                "notification": serializer.data
            }
            return Response(message, status=status.HTTP_201_CREATED)
        message = {
            "response": "Erreur de validation",
            "errors": serializer.errors
        }
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    #get notification by user en le rangeant par date de creation decroissante
    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'utilisateur': openapi.Schema(type=openapi.TYPE_INTEGER, description='Utilisateur'),
            },
            required=['utilisateur'],
        ),
        )
    @action(detail=False, methods=['post'])
    def get_notification_by_user(self, request):
        """
        Récupère les notifications associées à un utilisateur spécifique.
        Cette méthode extrait l'identifiant de l'utilisateur à partir de la requête et renvoie les notifications associées à cet utilisateur. Si l'identifiant de l'utilisateur n'est pas fourni, une réponse avec un message d'erreur et un statut HTTP 400 est renvoyée.

        Args:
            request (Request): La requête HTTP contenant les données nécessaires.
            {"utilisateur":1}
        
        Returns:
            Response code 200:
                [
                    {
                        "id": 1,
                        "utilisateur": 1,
                        "message": "Notification 1",
                        "date_creation": "2024-01-01T00:00:00Z",
                        "vu": false
                    },
                    ...
                ]
            
            Response code 400:
                {
                    "detail": "Aucune notification trouvée."
                }
        """
        
        utilisateur_id = request.data.get('utilisateur')
        if not utilisateur_id:
            return Response({"detail": "utilisateur est requis."}, status=status.HTTP_400_BAD_REQUEST)
        
        notifications = Notification.objects.filter(utilisateur=utilisateur_id).order_by('-date_creation')
        if notifications.exists():
            serializer = NotificationSerializer(notifications, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({"detail": "Aucune notification trouvée."}, status=status.HTTP_404_NOT_FOUND)
    #marquer une notification comme lu
    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'notification_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Notification'),
            },
            required=['notification_id'],
        ),
        )   
    @action(detail=False, methods=['post'])
    def marquer_notification_lu(self, request):
        """
        Marquer une notification comme lue.
        Cette méthode extrait l'identifiant de la notification à partir de la requête et met à jour le champ 'vu' de la notification correspondante à 'True'. Si l'identifiant de la notification n'est pas fourni, une réponse avec un message d'erreur et un statut HTTP 400 est renvoyée.

        Args:
            request (Request): La requête HTTP contenant les données nécessaires.
            {"notification_id":1}
        
        Returns:
            Response code 200:
                {
                    "response": "Notification marquée comme lue avec succès",
                    "notification": {
                        "id": 1,
                        "utilisateur": 1,
                        "message": "Notification 1",
                        "date_creation": "2024-01-01T00:00:00Z",
                        "vu": true
                    }
                }
            
            Response code 400:
                {
                    "detail": "Notification non trouvée."
                }
        """
        
        notification_id = request.data.get('notification_id')
        if not notification_id:
            return Response({"detail": "notification_id est requis."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.vu = True
            notification.save()
            serializer = NotificationSerializer(notification)
            return Response({"response": "Notification marquée comme lue avec succès", "notification": serializer.data}, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response({"detail": "Notification non trouvée."}, status=status.HTTP_404_NOT_FOUND)
        
        #nombre de notification non lues
    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'utilisateur': openapi.Schema(type=openapi.TYPE_INTEGER, description='Utilisateur'),
            },
            required=['utilisateur'],
        ),
        )
    @action(detail=False, methods=['post'])
    def nombre_notification_non_lue(self, request):
        """
        Récupère le nombre de notifications non lues associées à un utilisateur spécifique.
        Cette méthode extrait l'identifiant de l'utilisateur à partir de la requête et renvoie le nombre de notifications non lues associées à cet utilisateur. Si l'identifiant de l'utilisateur n'est pas fourni, une réponse avec un message d'erreur et un statut HTTP 400 est renvoyée.

        Args:
            request (Request): La requête HTTP contenant les données nécessaires.
            {"utilisateur":1}
        
        Returns:
            Response code 200:
                {
                    "nombre": 2
                }
            
            Response code 400:
                {
                    "detail": "Aucune notification trouvée."
                }
        """
        
        utilisateur_id = request.data.get('utilisateur')
        if not utilisateur_id:
            return Response({"detail": "utilisateur est requis."}, status=status.HTTP_400_BAD_REQUEST)
        
        nombre_notifications_non_lues = Notification.objects.filter(utilisateur=utilisateur_id, vu=False).count()
        return Response({"nombre": nombre_notifications_non_lues}, status=status.HTTP_200_OK)
    
class EvenementViewSet(viewsets.ModelViewSet):
    queryset = Evenement.objects.all()
    serializer_class = EvenementSerializer
    
    
    