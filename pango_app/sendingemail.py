from rest_framework.views import *
from .send_mail import envoi_email
from datetime  import datetime
    
    
def envoyer_email(email:str,nom:str,contrat:dict,motcle:str):
    subjet = "Test Email"
    template = 'index.html'
    context = {
                 'date': datetime.today(),
                    'email': email,
                    'nom_bailleur':nom,
                    
                    'contrat':contrat,
                    'mot_cle':motcle,
                }
    receivers = [email]

    has_send = envoi_email(
                    sujet=subjet,
                    desti=receivers,
                    template=template,
                    context=context
                    )
    if has_send:
        return True 
    else:
        return False