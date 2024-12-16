from django.contrib import admin
from .models import *


# Register your models here.

admin.site.register(Utilisateur)
admin.site.register(Adresse)
admin.site.register(BienImmobilier)
admin.site.register(ContratLocation)
admin.site.register(Payement)
admin.site.register(Evenement)
admin.site.register(Mot_cle)
admin.site.register(Notification)
admin.site.register(FilMessagerie)
admin.site.register(Message)

