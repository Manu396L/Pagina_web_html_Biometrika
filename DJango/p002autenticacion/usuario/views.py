from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth  import authenticate, login,logout
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import UserRegistrationForm, UserEditForm, LoginForm, ProfileEditForm, PersonalForm, UbicacionForm
from .models import Profile, Personal, Ubicacion

"""===================================
            MANEJO DE SESION
    =================================="""
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, 
                                username=cd['username'], 
                                password = cd['password']) 
            if user is not None:
                if user.is_active:
                    login(request, user)
                    next_url = request.POST.get('next', 'dashboard')  # Redirige al "next" o al dashboard
                    return redirect(next_url)  # Redirigir al dashboard
               
                else:
                    return HttpResponse('Usuario inactivo')
            else:
                return HttpResponse('Usuario no encontrado')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form':form})

def register_personal(request):             #En login
    if request.method == 'POST':
        form = PersonalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Empleado registrado correctamente.")
            return redirect('usuario:login')  # Redirige al login tras registro
    else:
        form = PersonalForm()

    return render(request, 'account/register_personal.html', {'form': form})

@login_required
def dashboard(request):
    ultimos_empleados = Personal.objects.order_by('fecha_ingreso')[:10]  # Últimos 10 agregados
    return render(request, 'account/dashboard.html', {
        'section': 'dashboard',
        'ultimos_empleados': ultimos_empleados,
    })

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form':user_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Perfil actualizado', 'succesful')
        else:
            messages.error(request, 'Error al actualizar el perfil')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html',{
        'user_form':user_form,
        'profile_form':profile_form
    })

def logged_out(request):
    logout(request)
    return render(request, 'registration/logged_out.html')

"""
=============================
        SEDES Y AREAS
============================="""

@login_required
def ubicaciones_view(request):
    from .models import Ubicacion
    from .forms import UbicacionForm

    ubicaciones = Ubicacion.objects.all().order_by('nombre_sede')
    form = UbicacionForm()

    if request.method == 'POST':
        form = UbicacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "La ubicación ha sido registrada correctamente.")
            return redirect('usuario:ubicaciones')
        else:
            messages.error(request, "Error al registrar la ubicación. Verifique los campos.")

    return render(request, 'account/ubicaciones.html', {
        'form': form,
        'ubicaciones': ubicaciones,
    }
    )

# Editar ubicación
def editar_ubicacion(request, id):
    ubicacion = get_object_or_404(Ubicacion, id=id)
    if request.method == 'POST':
        if 'guardar' in request.POST:
            form = UbicacionForm(request.POST, instance=ubicacion)
            if form.is_valid():
                form.save()
                return redirect('usuario:ubicaciones')
        elif 'cancelar' in request.POST:
            return redirect('usuario:ubicaciones')
    else:
        form = UbicacionForm(instance=ubicacion)

    return render(request, 'account/ubicacion_editar.html', {'form': form})


"""===================================
            PERSONAL
    =================================="""


@login_required
def gestion_personal(request):
    empleados = Personal.objects.all().order_by('apellido')
    form = PersonalForm()

    # Crear nuevo empleado
    if request.method == 'POST':
        if 'agregar' in request.POST:
            form = PersonalForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Empleado agregado correctamente.")
                return redirect('usuario:gestion_personal')

        # Editar empleado existente
        elif 'editar' in request.POST:
            empleado_id = request.POST.get('id')
            empleado = get_object_or_404(Personal, pk=empleado_id)
            form = PersonalForm(request.POST, instance=empleado)
            if form.is_valid():
                form.save()
                messages.success(request, "Empleado actualizado correctamente.")
                return redirect('usuario:gestion_personal')

        # Eliminar empleado
        elif 'eliminar' in request.POST:
            empleado_id = request.POST.get('id')
            empleado = get_object_or_404(Personal, pk=empleado_id)
            empleado.delete()
            messages.success(request, "Empleado eliminado correctamente.")
            return redirect('usuario:gestion_personal')

    return render(request, 'account/personal.html', {
        'empleados': empleados,
        'form': form,
    })

@login_required
def editar_personal(request, id):
    empleado = get_object_or_404(Personal, pk=id)
    form = PersonalForm(instance=empleado)

    if request.method == 'POST':
        if 'guardar' in request.POST:
            form = PersonalForm(request.POST, instance=empleado)
            if form.is_valid():
                form.save()
                messages.success(request, f"Empleado {empleado.apellido}, {empleado.nombre} actualizado correctamente.")
                return redirect('usuario:gestion_personal')

        elif 'cancelar' in request.POST:
            messages.info(request, "Edición cancelada.")
            return redirect('usuario:gestion_personal')

    return render(request, 'account/personal_editar.html', {
        'form': form,
        'empleado': empleado
    })