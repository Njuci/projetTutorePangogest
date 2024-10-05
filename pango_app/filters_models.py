import django_filters
from .models import *


class AdresseFilter(django_filters.FilterSet):
    class Meta:
        model = Adresse
        fields = '__all__'  # Cela inclut tous les champs du modèle Adresse

class UtilisateurFilter(django_filters.FilterSet):
    class Meta:
        model = Utilisateur
        fields = ['username', 'first_name', 'last_name', 'user_type']

class BienImmobilierFilter(django_filters.FilterSet):
    class Meta:
        model = BienImmobilier
        fields = ['adresse', 'surface', 'prix','utilisateur']

class ContratLocationFilter(django_filters.FilterSet):
    class Meta:
        model = ContratLocation
        fields = ['date_contrat','locataire__id' ,'date_debut', 'prix', 'encours','bien__utilisateur__id']

class PayementFilter(django_filters.FilterSet):
    class Meta:
        model = Payement
        fields = ['montant', 'date_payement', 'moyen_payement']

class EvenementFilter(django_filters.FilterSet):
    class Meta:
        model = Evenement
        fields = ['type_evenement', 'date_debut', 'date_fin', 'description']

class Mot_cleFilter(django_filters.FilterSet):
    class Meta:
        model = Mot_cle
        fields = ['mot_cle']