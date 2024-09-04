from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from datetime import timedelta

class Utilisateur(AbstractUser):
    USER_TYPES = [
        ('bailleur', 'Bailleur'),
        ('locataire', 'Locataire'),
    ]

    photo_url = models.URLField(max_length=500, blank=True, null=True)  # Stocke l'URL de la photo sur Firestore
    user_type = models.CharField(max_length=10, choices=USER_TYPES)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name','user_type','password']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Adresse(models.Model):
    ville = models.CharField(max_length=255)
    commune = models.CharField(max_length=255)
    quartier = models.CharField(max_length=255)
    cellule = models.CharField(max_length=255)
    avenue = models.CharField(max_length=255)
    num_av = models.CharField(max_length=10)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='adresses')

    def __str__(self):
        return f"{self.avenue}, {self.quartier}, {self.commune}, {self.ville}"

class BienImmobilier(models.Model):
    adresse = models.OneToOneField(Adresse, on_delete=models.CASCADE)
    surface = models.DecimalField(max_digits=10, decimal_places=2)
    photo_url = models.URLField(max_length=500, blank=True, null=True)  # Stocke l'URL de la photo du bien immobilier sur Firestore
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='biens')

    def clean(self):
        if self.utilisateur.user_type != 'bailleur':
            raise ValidationError('Seul un bailleur peut posséder un bien immobilier.')

    def __str__(self):
        return f"{self.description[:50]} - {self.prix} USD"

class ContratLocation(models.Model):
    date_contrat = models.DateField()
    date_debut = models.DateField()
    duree_contrat = models.IntegerField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    fichier = models.FileField(upload_to='contrats/')
    encours = models.BooleanField(default=False)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='contrats')
    bien = models.ForeignKey(BienImmobilier, on_delete=models.CASCADE, related_name='contrats')

    def clean(self):
        if self.utilisateur.user_type != 'locataire':
            raise ValidationError('Seuls les locataires peuvent signer un contrat de location.')

    def __str__(self):
        return f"Contrat de {self.utilisateur} pour {self.bien}"

class Payement(models.Model):
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
