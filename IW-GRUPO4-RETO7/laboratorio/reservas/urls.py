from django.urls import path
from .import views

urlpatterns = [
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('recursos/', views.lista_recursos, name='lista_recursos'),
    path('reservas/', views.lista_reservas, name='lista_reservas'),

    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('recursos/crear/', views.crear_recurso, name='crear_recurso'),
    path('reservas/crear/', views.crear_reserva, name='crear_reserva'),

    path('', views.index, name='index'),
]

