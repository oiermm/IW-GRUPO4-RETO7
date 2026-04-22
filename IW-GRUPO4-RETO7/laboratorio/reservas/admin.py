from django.contrib import admin
from .models import Usuario, Recurso, Reserva

# Register your models here.

admin.site.register(Usuario)
admin.site.register(Recurso)
admin.site.register(Reserva)