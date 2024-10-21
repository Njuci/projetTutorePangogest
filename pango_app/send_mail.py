import logging
from django.conf import settings
from django.core.mail import send_mail 
from django.template.loader import render_to_string


logger= logging.getLogger(__name__)

def envoi_email(sujet: str,desti : list, template :str, context:dict):
    try:
        msg= render_to_string(template,context)
        
        send_mail(
            sujet, 
            msg,
            settings.EMAIL_HOST_USER,
            desti,
            fail_silently=True,
            html_message=msg
        )
        return True
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de l'email: {e}")
    return False