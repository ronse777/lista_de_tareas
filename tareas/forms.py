from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Tarea

# Formulario de registro de usuarios
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

# Formulario de tareas
class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['nombre', 'prioridad', 'recordatorio']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Comprar leche'
            }),
            'prioridad': forms.Select(attrs={
                'class': 'form-select'
            }),
            'recordatorio': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }
        labels = {
            'nombre': 'Descripción',
            'prioridad': 'Prioridad',
            'recordatorio': 'Recordatorio'
        }
