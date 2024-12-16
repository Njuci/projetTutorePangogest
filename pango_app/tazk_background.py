from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


from django.utils import timezone
import pytz
from .models import ContratLocation, Notification

def notifier_locataire():
    contrats = ContratLocation.objects.all()
    now = timezone.now().date()  # Ensure now is defined here
    for contrat in contrats:
        if contrat.locataire:
            #calculer le nombre de jours restants avant la fin du contrat et la date de fin du contrat
            date_fin = contrat.date_contrat + timezone.timedelta(days=contrat.duree_mois * 30)  # Corrected line
            if now < date_fin:
                remaining_days = (date_fin - now).days
                message_locataire = f"""
                Bonjour {contrat.locataire.first_name} {contrat.locataire.last_name},\n
                
                Nous vous rappelons que votre contrat de location pour la maison située à {contrat.bien.adresse.ville} se termine dans {remaining_days} jours, le {date_fin}.\n
                
                Cordialement,\n
                Le bailleur de la maison\n
                {contrat.bien.utilisateur.first_name} {contrat.bien.utilisateur.last_name}\n    
                
                """
                
                Notification.objects.create(
                    utilisateur=contrat.locataire,
                    message=message_locataire,
                    vu=False
                )
                #marquer le contrat comme vu par le locataire
                message_bailleurs = f"""
                Bonjour {contrat.bien.utilisateur.first_name} {contrat.bien.utilisateur.last_name},\n
                
                Nous vous informons que le contrat de location pour la maison située à {contrat.bien.adresse.ville} se termine dans {remaining_days} jours, le {date_fin}.\n
                
                Cordialement,\n
                Votre équipe de gestion locative
                """
                
                Notification.objects.create(
                    utilisateur=contrat.bien.utilisateur,
                    message=message_bailleurs,
                    vu=False
                )
               
        else:
            #dites au bailleur de trouver que le locataire n'a pas encore accepté le contrat et 
            # le systeme va supprimer le contrat dans 2 jours à partir de la date de creation
            # et le bailleur doit le refaire s;il veut toujours louer le bien
            #supprimer le contrat si le locataire n'a pas encore accepté le contrat et que le 2 jours sont passés
            if now > contrat.date_contrat + timezone.timedelta(days=200):
                
                Notification.objects.create(
                    utilisateur=contrat.bien.utilisateur,
                    message=f"Le contrat de location pour la maison située à {contrat.bien.adresse.ville} a été supprimé car le locataire n'a pas encore accepté le contrat.",
                    vu=False
                )
                contrat.delete()
            else:
                print("Le locataire n'a pas encore accepté le contrat")
                message_bailleurs = f"""
                    Bonjour {contrat.bien.utilisateur.first_name} {contrat.bien.utilisateur.last_name},\n
                    Nous vous informons que le locataire n'a pas encore accepté le contrat de location pour la maison située à {contrat.bien.adresse.ville}.\n
                    Le contrat sera supprimé dans 2 jours à partir de la date de création.\n
                    Cordialement,\n
                    Votre équipe de gestion locative
                    """
                Notification.objects.create(
                    utilisateur=contrat.bien.utilisateur,
                    message=message_bailleurs,
                    vu=False
                )
# 

def start_scheduler():
    scheduler = BackgroundScheduler()
    central_africa_tz = pytz.timezone("Africa/Lubumbashi")
    scheduler.add_job(
        notifier_locataire,
        trigger=CronTrigger(hour=11,minute=29,timezone=central_africa_tz),  # Par exemple, toutes les 60 secondes
        id="notifier_locataire",  # ID unique pour éviter les doublons
        replace_existing=True
    )
    scheduler.start()