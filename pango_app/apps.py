from django.apps import AppConfig

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

class PangoAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pango_app'

    def ready(self):
        from .tazk_background import  start_scheduler
        
        start_scheduler()
        
        
