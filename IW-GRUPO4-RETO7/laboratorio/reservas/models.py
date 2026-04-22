from django.db import models

# Create your models here.

class Usuario(models.Model):
    dni = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nombre} {self.apellidos} ({self.dni})"
    

class Recurso(models.Model):
    ESTADOS = [
        ('disponible', 'Disponible'),
        ('mantenimiento', 'En mantenimiento'),
        ('fuera_servicio', 'Fuera de servicio'),
    ]

    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=150)
    tipo = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=150)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='disponible')

    responsable_tecnico = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recursos_responsables'
    )

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"
    


class Reserva(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]

    codigo_reserva = models.CharField(max_length=50, unique=True)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    finalidad = models.TextField()

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='reservas'
    )

    recurso = models.ForeignKey(
        Recurso,
        on_delete=models.CASCADE,
        related_name='reservas'
    )

    def __str__(self):
        return f"Reserva {self.codigo_reserva} - {self.recurso.nombre}"