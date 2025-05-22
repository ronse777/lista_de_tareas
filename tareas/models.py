from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.exceptions import ValidationError

class Tarea(models.Model):
    PRIORIDADES = [
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    prioridad = models.CharField(max_length=50, choices=PRIORIDADES, default='media')
    prioridad_valor = models.IntegerField(default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    completada = models.BooleanField(default=False)
    fecha_completado = models.DateTimeField(null=True, blank=True)
    recordatorio = models.DateTimeField(null=True, blank=True)
    reminder_sent = models.BooleanField(default=False)

    def clean(self):
        if self.recordatorio and self.recordatorio < timezone.now():
            raise ValidationError('La fecha del recordatorio debe estar en el futuro.')

    def save(self, *args, **kwargs):
        # Solo ejecutar validación si no se indica lo contrario
        if not kwargs.pop('skip_validation', False):
            self.full_clean()
        prioridad_map = {'alta': 1, 'media': 2, 'baja': 3}
        self.prioridad_valor = prioridad_map.get(self.prioridad, 2)
        super().save(*args, **kwargs)

    def marcar_como_completada(self):
        self.completada = True
        self.fecha_completado = timezone.now()
        self.save(skip_validation=True)  # ← muy importante

    def enviar_recordatorio(self):
        if self.recordatorio and not self.reminder_sent:
            try:
                email = EmailMessage(
                    subject=f"Recordatorio: {self.nombre}",
                    body=f"Tienes una tarea pendiente: {self.nombre}\nFecha recordatorio: {self.recordatorio}",
                    from_email=settings.EMAIL_HOST_USER,
                    to=[self.usuario.email],
                )
                email.content_subtype = "plain"
                email.encoding = "utf-8"
                email.send()
                self.reminder_sent = True
                self.save(skip_validation=True)
            except Exception as e:
                print(f"Error enviando recordatorio: {e}")

    def __str__(self):
        return f"{self.nombre} ({self.get_prioridad_display()})"

    class Meta:
        ordering = ['prioridad_valor', 'recordatorio']
