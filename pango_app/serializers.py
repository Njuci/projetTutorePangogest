from rest_framework.serializers import ModelSerializer
from .models import *

class UtilisateurSerializer(ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = '__all__'
        
        
class ContratLocationSerializer(ModelSerializer):
    class Meta:
        model = ContratLocation
        fields = '__all__'
        
class EvenementSerializer(ModelSerializer):
    class Meta:
        model = Evenement
        fields = '__all__'
        
class AdresseSerializer(ModelSerializer):
    class Meta:
        model = Adresse
        fields = '__all__'
        
class BienImmobilierSerializer(ModelSerializer):
    class Meta:
        model = BienImmobilier
        fields = '__all__'
        
class PayementSerializer(ModelSerializer):
    class Meta:
        model = Payement
        fields = '__all__'
        
 
        
class EvenementSerializer(ModelSerializer):
    class Meta:
        model = Evenement
        fields = '__all__'

class Mot_cleSerializer(ModelSerializer):
    class Meta:
        model = Mot_cle
        fields = '__all__'