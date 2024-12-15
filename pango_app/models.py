from django.contrib.auth.models import AbstractUser,Group,Permission
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from datetime import timedelta

# Création des modèles pour l'application Pango

class Adresse(models.Model):
    # Modèle pour stocker les adresses des biens immobiliers
    ville = models.CharField(max_length=255,default='Bukavu')
    commune = models.CharField(max_length=255)
    quartier = models.CharField(max_length=255)
    cellule = models.CharField(max_length=255,null=True)
    avenue = models.CharField(max_length=255,null=True)
    num_av = models.CharField(max_length=10,null=True)
    def __str__(self):
        return f"{self.avenue}, {self.quartier}, {self.commune}, {self.ville}"

class Utilisateur(AbstractUser):
    USER_TYPES = [
        ('bailleur', 'Bailleur'),
        ('locataire', 'Locataire'),
    ]
    # Champs supplémentaires pour les utilisateurs

    photo_url = models.URLField(max_length=500, blank=True, null=True)  # Stocke l'URL de la photo sur Firestore
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    telephone=models.CharField(max_length=14)
    id_adresse=models.ForeignKey('Adresse',on_delete=models.CASCADE,null=True)
    groups = models.ManyToManyField(Group, related_name='myuser_set', blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name='utilisateur_set', blank=True
    )

    USERNAME_FIELD = 'username'#Champ pour l'authentification
    REQUIRED_FIELDS = ['first_name', 'last_name','user_type','password','email','telephone'] #Champs obligatoires pour la création d'un utilisateur il y a des champs par défaut herité de la classe AbstractUser

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class BienImmobilier(models.Model):
    # Modèle pour stocker les biens immobiliers
    adresse = models.OneToOneField(Adresse, on_delete=models.CASCADE)#L'adresse du bien immobilier
    surface = models.CharField(max_length=10)#La surface du bien immobilier
    photo_url = models.URLField(max_length=500, blank=True, null=True)  # Stocke l'URL de la photo du bien immobilier sur Firestore
    description = models.TextField() #Description du bien immobilier
    prix = models.DecimalField(max_digits=10, decimal_places=2)#Le prix du bien immobilier
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='biens')#Le propriétaire du bien immobilier

    def clean(self):
        if self.utilisateur.user_type != 'bailleur': #Vérifie si le propriétaire du bien immobilier est un bailleur
            raise ValidationError('Seul un bailleur peut posséder un bien immobilier.')#Message d'erreur

    def __str__(self):
        return f"{self.description[:50]} - {self.prix} USD"

class ContratLocation(models.Model):
    """ Modèle pour stocker les contrats de location """
    date_contrat = models.DateField() #Date de signature du contrat
    date_debut = models.DateField()#Date de début du contrat
    prix = models.DecimalField(max_digits=10, decimal_places=2)#Le prix du contrat
    fichier = models.URLField(max_length=500, blank=True, null=True)#Le fichier du contrat s'il y en a
    duree_mois = models.IntegerField()#La durée du contrat en mois
    encours = models.BooleanField(default=False) #Indique si le contrat est en cours ou non
    locataire = models.ForeignKey(Utilisateur, on_delete=models.CASCADE,null=True,related_name='contrats') #Le locataire du bien immobilier le locateur 
    bien = models.ForeignKey(BienImmobilier, on_delete=models.CASCADE, related_name='contrats') #Le bien immobilier loué par le locataire 
    def clean(self):#Vérifie si le locataire est un locataire
        if self.locataire and self.locataire.user_type != 'locataire':
            raise ValidationError('Seuls les locataires peuvent signer un contrat de location.')

    def __str__(self):
        if self.locataire:
            return f"Contrat de {self.locataire.first_name} pour {self.bien}"
        else:
            return f"Contrat pour {self.bien}"
        

class Mot_cle(models.Model):
    # Modèle pour stocker les mots-clés
    locataire=models.ForeignKey( Utilisateur, on_delete=models.CASCADE,null=True ,related_name='mots_cles')
    email=models.EmailField(null=True)
    contrat = models.ForeignKey(ContratLocation, on_delete=models.CASCADE, related_name='mots_cles')
    mot_cle = models.CharField(max_length=255)
    
    def clean(self):
        if self.locataire and self.locataire.user_type != 'locataire': 
            raise ValidationError('Seuls les locataires peuvent ajouter des mots-clés.')
    
    
    def __str__(self):
        return self.mot_cle
class Payement(models.Model):
    # Modèle pour stocker les payements effectués par les locataires
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_payement = models.DateField()
    moyen_payement = models.CharField(max_length=255)
    contrat = models.ForeignKey(ContratLocation, on_delete=models.CASCADE, related_name='payements')

    def __str__(self):
        return f"Payement de {self.montant} USD le {self.date_payement}"
class Evenement(models.Model):
    TYPE_EVENEMENT = [
        ('visite', 'Visite'),
        ('convocation', 'Convocation'),
        ('grace', 'Mesure de Grâce'),
        
    ]

    type_evenement = models.CharField(max_length=50, choices=TYPE_EVENEMENT)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    description = models.TextField()
    contrat = models.ForeignKey('ContratLocation', on_delete=models.CASCADE, related_name='evenements')
    notifications = models.BooleanField(default=True)

    # Champs pour gérer les intervalles de notifications en jours
    MODIFIER_JOURS_CHOICES = [
        (15, '15 jours avant'),
        (10, '10 jours avant'),
        (5, '5 jours avant'),
        (1, '1 jour avant'),
    ]
    modifier_jour = models.IntegerField(choices=MODIFIER_JOURS_CHOICES, default=15)

    # Champs pour suivre l'état de visualisation
    vu_par_bailleur = models.BooleanField(default=False)
    vu_par_locataire = models.BooleanField(default=False)

    def declencher_notifications(self):
        maintenant = timezone.now()

        if self.notifications and maintenant >= self.date_debut - timedelta(days=self.modifier_jour):
            self.envoyer_notification(f"{self.modifier_jour} jours avant l'événement")

    def envoyer_notification(self, message):
        
        # Logique pour envoyer la notification (email, SMS, etc.)
        print(f"Notification: {message} pour l'événement {self.type_evenement}")

    def __str__(self):
        return f"{self.type_evenement} du {self.date_debut} au {self.date_fin}"

    def marquer_comme_vu(self, par_bailleur=False, par_locataire=False):
        if par_bailleur:
            self.vu_par_bailleur = True 
        if par_locataire:
            self.vu_par_locataire = True
        self.save()

    def est_vu_par_autre_partie(self):
        # Logique pour vérifier si l'événement a été vu par l'autre partie
        if self.vu_par_bailleur and self.vu_par_locataire:
            return True
        return False

class Notification(models.Model):
    """ Modèle pour stocker les notifications """
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    vu = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification pour {self.utilisateur} - {self.message[:50]}"

class FilMessagerie(models.Model):
    contrat = models.OneToOneField(ContratLocation, on_delete=models.CASCADE, related_name='fil_messagerie')

    def __str__(self):
        return f"Fil de messages pour le contrat {self.contrat}"

class Message(models.Model):
    date_heure = models.DateTimeField(auto_now_add=True)
    expediteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='messages_envoyes')
    destinataire = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='messages_recus')
    contenu = models.TextField()
    fil_messagerie = models.ForeignKey(FilMessagerie, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return f"Message de {self.expediteur} à {self.destinataire} le {self.date_heure}"
''' 



'''