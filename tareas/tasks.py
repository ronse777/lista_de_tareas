from django.utils import timezone  # ← IMPORTANTE
from celery import shared_task
from .models import Tarea
from django.core.mail import send_mail
from django.conf import settings

@shared_task(name="tareas.enviar_recordatorio_email")
def enviar_recordatorio_email(asunto, mensaje, destinatario):
    try:
        send_mail(
            asunto,
            mensaje,
            settings.EMAIL_HOST_USER,
            [destinatario],
            fail_silently=False,
        )
        return f"Correo enviado a {destinatario}"
    except Exception as e:
        return f"Error: {str(e)}"

@shared_task(name="tareas.verificar_recordatorios")
def verificar_recordatorios():
    ahora = timezone.now()
    tareas = Tarea.objects.filter(
        recordatorio__lte=ahora,
        reminder_sent=False,
        completada=False
    )
    for tarea in tareas:
        tarea.enviar_recordatorio()
