from django.urls import path
from . import views

app_name = 'tareas'

urlpatterns = [
    path('', views.index, name='index'),
    path('registro/', views.registro, name='registro'),
    path('eliminar/<int:tarea_id>/', views.eliminar_tarea, name='eliminar_tarea'),
    path('completar/<int:tarea_id>/', views.completar_tarea, name='completar_tarea'),
]
