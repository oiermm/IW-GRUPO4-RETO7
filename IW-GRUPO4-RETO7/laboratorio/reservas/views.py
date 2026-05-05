from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario, Recurso, Reserva
from .forms import UsuarioForm, RecursoForm, ReservaForm

# ---------- LISTADOS ----------
def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'reservas/lista_usuarios.html', {'usuarios': usuarios})

def lista_recursos(request):
    recursos = Recurso.objects.all()
    return render(request, 'reservas/lista_recursos.html', {'recursos': recursos})

def lista_reservas(request):
    reservas = Reserva.objects.all()
    return render(request, 'reservas/lista_reservas.html', {'reservas': reservas})


# ---------- CREAR ----------
def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'reservas/crear_usuario.html', {'form': form})

def crear_recurso(request):
    if request.method == 'POST':
        form = RecursoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_recursos')
    else:
        form = RecursoForm()
    return render(request, 'reservas/crear_recurso.html', {'form': form})

def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_reservas')
    else:
        form = ReservaForm()
    return render(request, 'reservas/crear_reserva.html', {'form': form})

def index(request):
    return render(request, 'reservas/index.html')

def detalle_reserva(request, id):
    reserva = Reserva.objects.get(id=id)
    return render(request, 'reservas/detalle_reserva.html', {'reserva': reserva})

# ---------- EDITAR ----------
def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    
    if request.method == 'POST':
        
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
        
            return redirect('lista_usuarios') 
    else:
        
        form = UsuarioForm(instance=usuario)
        
    return render(request, 'reservas/editar_usuario.html', {'form': form, 'usuario': usuario})

def editar_reserva(request, id):
    reserva = get_object_or_404(Reserva, id=id)

    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            return redirect('lista_reservas')
    else:
        form = ReservaForm(instance=reserva)

    return render(request, 'reservas/editar_reserva.html', {'form': form})

def editar_recurso(request, id):
    recurso = get_object_or_404(Recurso, id=id)

    if request.method == 'POST':
        form = RecursoForm(request.POST, instance=recurso)
        if form.is_valid():
            form.save()
            return redirect('lista_recursos')
    else:
        form = RecursoForm(instance=recurso)

    return render(request, 'reservas/editar_recurso.html', {'form': form})


# ---------- ELIMINAR ----------

def eliminar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)

    if request.method == 'POST':
        usuario.delete()
        return redirect('lista_usuarios')

    return render(request, 'reservas/eliminar_usuario.html', {'usuario': usuario})

def eliminar_recurso(request, id):
    recurso = get_object_or_404(Recurso, id=id)

    if request.method == 'POST':
        recurso.delete()
        return redirect('lista_recursos')

    return render(request, 'reservas/eliminar_recurso.html', {'recurso': recurso})

def eliminar_reserva(request, id):
    reserva = get_object_or_404(Reserva, id=id)

    if request.method == 'POST':
        reserva.delete()
        return redirect('lista_reservas')

    return render(request, 'reservas/eliminar_reserva.html', {'reserva': reserva})