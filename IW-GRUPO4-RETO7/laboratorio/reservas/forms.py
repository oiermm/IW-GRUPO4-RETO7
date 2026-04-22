from django import forms
from .models import Usuario, Recurso, Reserva


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'


class RecursoForm(forms.ModelForm):
    class Meta:
        model = Recurso
        fields = '__all__'


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = '__all__'