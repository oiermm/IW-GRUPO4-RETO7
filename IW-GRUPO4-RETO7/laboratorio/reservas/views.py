import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Usuario, Recurso, Reserva
from .forms import UsuarioForm, RecursoForm, ReservaForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import status
from .serializers import ReservaSerializer, RecursoSerializer, UsuarioSerializer
from .authentication import URLJWTAuthentication 

logger = logging.getLogger('reservas')


def index(request):
    return render(request, 'reservas/index.html')

def login_view(request):
    return render(request, 'reservas/login.html')

# ---------- LISTADOS ----------
def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'reservas/lista_usuarios.html', {'usuarios': usuarios})

def lista_recursos(request):
    recursos = Recurso.objects.all()
    return render(request, 'reservas/lista_recursos.html', {'recursos': recursos})

def lista_reservas(request):
    return render(request, 'reservas/lista_reservas.html')

def detalle_reserva(request, id):
    reserva = get_object_or_404(Reserva, id=id)
    return render(request, 'reservas/detalle_reserva.html', {'reserva': reserva})

# ---------- CREAR ----------
def crear_usuario(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info(f"Usuario creado: {form.cleaned_data['nombre']}")
            return redirect(f'/usuarios/?token={token}')
    else:
        form = UsuarioForm()
    return render(request, 'reservas/crear_usuario.html', {'form': form})

def crear_recurso(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        form = RecursoForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info(f"Recurso creado: {form.cleaned_data['nombre']}")
            return redirect(f'/recursos/?token={token}')
    else:
        form = RecursoForm()
    return render(request, 'reservas/crear_recurso.html', {'form': form})

def crear_reserva(request):
    return render(request, 'reservas/crear_reserva.html')

# ---------- EDITAR ----------
def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        token = request.GET.get('token') or request.POST.get('token')
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect(f'/usuarios/?token={token}')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'reservas/editar_usuario.html', {'form': form, 'usuario': usuario})

def editar_reserva(request, id):
    reserva = get_object_or_404(Reserva, id=id)
    if request.method == 'POST':
        token = request.GET.get('token') or request.POST.get('token')
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            return redirect(f'/reservas/?token={token}')
    else:
        form = ReservaForm(instance=reserva)
    return render(request, 'reservas/editar_reserva.html', {'form': form})

def editar_recurso(request, id):
    recurso = get_object_or_404(Recurso, id=id)
    if request.method == 'POST':
        token = request.GET.get('token') or request.POST.get('token')
        form = RecursoForm(request.POST, instance=recurso)
        if form.is_valid():
            form.save()
            return redirect(f'/recursos/?token={token}')
    else:
        form = RecursoForm(instance=recurso)
    return render(request, 'reservas/editar_recurso.html', {'form': form})

# ---------- ELIMINAR ----------
def eliminar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        token = request.GET.get('token') or request.POST.get('token')
        usuario.delete()
        return redirect(f'/usuarios/?token={token}')
    return render(request, 'reservas/eliminar_usuario.html', {'usuario': usuario})

def eliminar_recurso(request, id):
    recurso = get_object_or_404(Recurso, id=id)
    if request.method == 'POST':
        token = request.GET.get('token') or request.POST.get('token')
        recurso.delete()
        return redirect(f'/recursos/?token={token}')
    return render(request, 'reservas/eliminar_recurso.html', {'recurso': recurso})

def eliminar_reserva(request, id):
    reserva = get_object_or_404(Reserva, id=id)
    if request.method == 'POST':
        token = request.GET.get('token') or request.POST.get('token')
        reserva.delete()
        return redirect(f'/reservas/?token={token}')
    return render(request, 'reservas/eliminar_reserva.html', {'reserva': reserva})


# ══════════════════════════════════════════
#  API VIEWS
# ══════════════════════════════════════════

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [URLJWTAuthentication]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            logger.info(f"Login exitoso: {username}")
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'username': user.username,
            })

        logger.warning(f"Login fallido: {username}")
        return Response(
            {'error': 'Credenciales incorrectas'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class MiPerfilAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [URLJWTAuthentication]
    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
        })


class ReservaAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [URLJWTAuthentication]
    def get(self, request):
        reservas = Reserva.objects.all().order_by('fecha', 'hora_inicio')

        recurso_q = request.query_params.get('recurso', '')
        fecha_q = request.query_params.get('fecha', '')

        if recurso_q:
            reservas = reservas.filter(recursos__nombre__icontains=recurso_q)
            logger.debug(f"Busqueda por recurso: {recurso_q}")
        if fecha_q:
            reservas = reservas.filter(fecha=fecha_q)
            logger.debug(f"Busqueda por fecha: {fecha_q}")

        paginator = Paginator(reservas, 5)
        page_num = request.query_params.get('page', 1)
        page = paginator.get_page(page_num)

        serializer = ReservaSerializer(page.object_list, many=True)
        return Response({
            'results': serializer.data,
            'total_pages': paginator.num_pages,
            'current_page': page.number,
            'total': paginator.count,
        })

    def post(self, request):
        serializer = ReservaSerializer(data=request.data)
        if serializer.is_valid():
            fecha = serializer.validated_data.get('fecha')
            hora_inicio = serializer.validated_data.get('hora_inicio')
            hora_fin = serializer.validated_data.get('hora_fin')
            recursos = serializer.validated_data.get('recursos_ids', [])
            
            recursos_ids = [r.id for r in recursos]

            conflicto = Reserva.objects.filter(
                fecha=fecha,
                recursos__in=recursos_ids,
                hora_inicio__lt=hora_fin,
                hora_fin__gt=hora_inicio,
            ).exists()

            if conflicto:
                logger.warning(f"Conflicto de horario detectado en fecha {fecha}")
                return Response(
                    {'error': 'Ya existe una reserva para ese recurso en ese horario'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            reserva = serializer.save()
            logger.info(f"Reserva creada: {reserva.codigo_reserva}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"Error al crear reserva: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReservaDetalleAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [URLJWTAuthentication]
    def get(self, request, id):
        reserva = get_object_or_404(Reserva, id=id)
        return Response(ReservaSerializer(reserva).data)

    def put(self, request, id):
        reserva = get_object_or_404(Reserva, id=id)
        serializer = ReservaSerializer(reserva, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Reserva editada: {reserva.codigo_reserva}")
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        reserva = get_object_or_404(Reserva, id=id)
        logger.warning(f"Reserva eliminada: {reserva.codigo_reserva}")
        reserva.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecursoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    authentication_classes = [URLJWTAuthentication]
    def get(self, request):
        recursos = Recurso.objects.all()
        serializer = RecursoSerializer(recursos, many=True)
        return Response(serializer.data)


class UsuarioAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [URLJWTAuthentication]
    def get(self, request):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)
    
