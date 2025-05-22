import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lista_de_tareas.settings')
application = get_wsgi_application()
application = WhiteNoise(application, root='static/')  # Para archivos estáticos