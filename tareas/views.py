from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.utils import timezone
from .models import Tarea
from .forms import TareaForm, RegistroForm

# Vista de registro
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tareas:index')
    else:
        form = RegistroForm()
    return render(request, 'registration/registro.html', {'form': form})

# Página principal con formulario y lista de tareas
@login_required
def index(request):
    tareas_pendientes = Tarea.objects.filter(
        usuario=request.user,
        completada=False
    ).order_by('prioridad_valor')

    tareas_completadas = Tarea.objects.filter(
        usuario=request.user,
        completada=True
    ).order_by('-fecha_completado')

    if request.method == "POST":
        form = TareaForm(request.POST)
        if form.is_valid():
            nueva_tarea = form.save(commit=False)
            nueva_tarea.usuario = request.user
            nueva_tarea.save()
            return redirect('tareas:index')
    else:
        form = TareaForm()

    return render(request, 'tareas/index.html', {
        'form': form,
        'tareas_pendientes': tareas_pendientes,
        'tareas_completadas': tareas_completadas
    })

# Eliminar tarea
@login_required
def eliminar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id, usuario=request.user)
    tarea.delete()
    return redirect('tareas:index')

# Marcar tarea como completada
@login_required
def completar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id, usuario=request.user)
    tarea.completada = True
    tarea.fecha_completado = timezone.now()
    tarea.save(skip_validation=True)
    return redirect('tareas:index')
