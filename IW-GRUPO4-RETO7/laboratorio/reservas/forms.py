from django import forms
from .models import Usuario, Recurso, Reserva
from django.core.exceptions import ValidationError


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

        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time'}),
            'recursos': forms.CheckboxSelectMultiple(),
        }

    def clean(self):

        cleaned_data = super().clean()

        fecha = cleaned_data.get('fecha')
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')
        recursos = cleaned_data.get('recursos')

        if not fecha or not hora_inicio or not hora_fin or not recursos:
            return cleaned_data

        # Validación básica
        if hora_inicio >= hora_fin:
            raise ValidationError(
                "La hora de inicio debe ser anterior a la de fin."
            )

        # Buscar conflictos
        conflictos = Reserva.objects.filter(
            fecha=fecha,
            recursos__in=recursos
        ).exclude(id=self.instance.id).distinct()

        # Comprobar solapamientos
        for r in conflictos:
            if hora_inicio < r.hora_fin and hora_fin > r.hora_inicio:
                raise ValidationError(
                    "Este horario no está disponible."
                )

        return cleaned_data