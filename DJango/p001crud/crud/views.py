from django.shortcuts import render, redirect, get_object_or_404
from .models import Task,Edificio
from .forms import TaskForm, EdificioForm


def task_list_and_create(request):

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crud:crud_list')
    else:
        form = TaskForm()
    #tasks = Task.objects.all()
    complete_tasks = Task.objects.filter(is_completed=True)
    incomplete_tasks = Task.objects.filter(is_completed=False)

    return render(request, 'task_list.html', {
        'form':form,
        #'tasks':tasks
        'complete_tasks':complete_tasks,
        'incomplete_tasks':incomplete_tasks
    })

def update_nombre_empleado(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.is_completed = not task.is_completed
    task.save()
    return redirect('crud:crud_list')

    
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    initial_data = {
            'title': task.title,
            'description': task.description,
        }
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('crud:crud_list')
    else:
        form = TaskForm(instance=task, initial=initial_data)
    
    return render(request, 'edit_task.html', {'form': form})

def delete_task(request, task_id):
    if request.method == 'POST':
        task = Task.objects.get(id=task_id)
        task.delete()
        return redirect('crud:crud_list')
    
# Vista para listar los edificios
def listar_edificios(request):
    edificios = Edificio.objects.all()
    return render(request, 'edificios/listar.html', {'edificios': edificios})

# Vista para crear un nuevo edificio
def crear_edificio(request):
    if request.method == 'POST':
        form = EdificioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crud:listar_edificios')
    else:
        form = EdificioForm()
    return render(request, 'edificios/crear.html', {'form': form})

# Vista para editar un edificio
def editar_edificio(request, pk):
    edificio = get_object_or_404(Edificio, pk=pk)
    if request.method == 'POST':
        form = EdificioForm(request.POST, instance=edificio)
        if form.is_valid():
            form.save()
            return redirect('crud:listar_edificios')
    else:
        form = EdificioForm(instance=edificio)
    return render(request, 'edificios/editar.html', {'form': form})

# Vista para eliminar un edificio
def eliminar_edificio(request, pk):
    edificio = get_object_or_404(Edificio, pk=pk)
    if request.method == 'POST':
        edificio.delete()
        return redirect('crud:listar_edificios')
    return render(request, 'edificios/eliminar.html', {'edificio': edificio})