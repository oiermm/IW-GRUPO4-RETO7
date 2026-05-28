from rest_framework import serializers
from .models import Usuario, Recurso, Reserva


class UsuarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usuario
        fields = [
            'id',
            'dni',
            'nombre',
            'apellidos',
            'email',
            'telefono',
        ]


class RecursoSerializer(serializers.ModelSerializer):
    responsable_tecnico = serializers.StringRelatedField()

    class Meta:
        model = Recurso
        fields = [
            'id',
            'codigo',
            'nombre',
            'tipo',
            'ubicacion',
            'estado',
            'responsable_tecnico',
        ]


class ReservaSerializer(serializers.ModelSerializer):

    usuario = serializers.StringRelatedField(read_only=True)
    recursos = serializers.StringRelatedField(many=True, read_only=True)

    recursos_ids = serializers.PrimaryKeyRelatedField(
        queryset=Recurso.objects.all(),
        many=True,
        write_only=True
    )

    usuario_id = serializers.PrimaryKeyRelatedField(
        queryset=Usuario.objects.all(),
        source='usuario',
        write_only=True
    )

    class Meta:
        model = Reserva
        fields = [
            'id',
            'codigo_reserva',
            'fecha',
            'hora_inicio',
            'hora_fin',
            'estado',
            'finalidad',
            'usuario',
            'usuario_id',
            'recursos',
            'recursos_ids',
        ]

    def create(self, validated_data):
        recursos = validated_data.pop('recursos_ids')
        reserva = Reserva.objects.create(**validated_data)
        reserva.recursos.set(recursos)
        return reserva

    def update(self, instance, validated_data):
        recursos = validated_data.pop('recursos_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if recursos is not None:
            instance.recursos.set(recursos)
        return instance