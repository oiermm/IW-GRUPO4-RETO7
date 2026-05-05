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
    path('reservas/<int:id>/', views.detalle_reserva, name='detalle_reserva'),
    
    path('usuarios/editar/<int:id>/', views.editar_usuario, name='editar_usuario'),
    path('recursos/editar/<int:id>/', views.editar_recurso, name='editar_recurso'),
    path('reservas/editar/<int:id>/', views.editar_reserva, name='editar_reserva'),
    
    path('usuarios/<int:id>/eliminar/', views.eliminar_usuario, name='eliminar_usuario'),
    path('recursos/<int:id>/eliminar/', views.eliminar_recurso, name='eliminar_recurso'),
    path('reservas/<int:id>/eliminar/', views.eliminar_reserva, name='eliminar_reserva'),
]

