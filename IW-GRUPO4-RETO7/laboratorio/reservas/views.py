from django.shortcuts import render, redirect
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
