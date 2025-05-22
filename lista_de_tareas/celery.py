import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lista_de_tareas.settings')

app = Celery('lista_de_tareas')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Configuración de tareas periódicas (usando django-celery-beat)
app.conf.beat_schedule = {
    'verificar-recordatorios-cada-minuto': {
        'task': 'tareas.tasks.verificar_recordatorios',
        'schedule': crontab(minute='*/1'),
    },
}