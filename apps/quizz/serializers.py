from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Quizz, Pregunta, Opcion, PerfilJugador, Partida1v1

class OpcionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Opcion
        fields = ['id', 'texto', 'es_correcta']


class PreguntaSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    opciones = OpcionSerializer(many=True)
    quizz_id = serializers.PrimaryKeyRelatedField(
        queryset=Quizz.objects.all(), source='quizz', write_only=True, required=False
    )

    class Meta:
        model = Pregunta
        fields = ['id', 'texto', 'quizz_id', 'opciones']

    def create(self, validated_data):
        validated_data.pop('id', None)
        opciones = validated_data.pop('opciones', [])
        pregunta = Pregunta.objects.create(**validated_data)
        Opcion.objects.bulk_create(
            [Opcion(pregunta=pregunta, **{k: v for k, v in opcion.items() if k != 'id'}) for opcion in opciones]
        )
        return pregunta

    def update(self, instance, validated_data):
        opciones = validated_data.pop('opciones', None)
        for campo, valor in validated_data.items():
            setattr(instance, campo, valor)
        instance.save()

        if opciones is not None:
            opciones_actuales = {opcion.id: opcion for opcion in instance.opciones.all()}
            ids_recibidos = set()
            for opcion_data in opciones:
                opcion_id = opcion_data.pop('id', None)
                if opcion_id in opciones_actuales:
                    opcion = opciones_actuales[opcion_id]
                    for campo, valor in opcion_data.items():
                        setattr(opcion, campo, valor)
                    opcion.save()
                    ids_recibidos.add(opcion_id)
                else:
                    Opcion.objects.create(pregunta=instance, **opcion_data)
            instance.opciones.exclude(id__in=ids_recibidos).delete()
        return instance


class QuizzSerializer(serializers.ModelSerializer):
    preguntas = PreguntaSerializer(many=True)

    class Meta:
        model = Quizz
        fields = ['id', 'titulo', 'descripcion', 'creado_en', 'preguntas']

    def create(self, validated_data):
        preguntas = validated_data.pop('preguntas', [])
        quizz = Quizz.objects.create(**validated_data)
        for pregunta_data in preguntas:
            pregunta_data['quizz'] = quizz
            PreguntaSerializer().create(pregunta_data)
        return quizz

    def update(self, instance, validated_data):
        preguntas = validated_data.pop('preguntas', None)
        instance = super().update(instance, validated_data)
        if preguntas is not None:
            for pregunta_data in preguntas:
                pregunta_id = pregunta_data.pop('id', None)
                if pregunta_id:
                    pregunta = instance.preguntas.get(id=pregunta_id)
                    PreguntaSerializer().update(pregunta, pregunta_data)
                else:
                    pregunta_data['quizz'] = instance
                    PreguntaSerializer().create(pregunta_data)
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class PerfilJugadorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = PerfilJugador
        fields = ['id', 'user', 'puntos_experiencia', 'victorias_1v1', 'derrotas_1v1']


class Partida1v1Serializer(serializers.ModelSerializer):
    jugador_1 = UserSerializer(read_only=True)
    jugador_2 = UserSerializer(read_only=True)
    ganador = UserSerializer(read_only=True)
    quizz = QuizzSerializer(read_only=True)
    
    quizz_id = serializers.PrimaryKeyRelatedField(
        queryset=Quizz.objects.all(), source='quizz', write_only=True
    )

    class Meta:
        model = Partida1v1
        fields = [
            'id', 'quizz', 'quizz_id', 'jugador_1', 'jugador_2', 
            'puntaje_j1', 'puntaje_j2', 'estado', 'ganador', 'creado_en'
        ]
        read_only_fields = ['puntaje_j1', 'puntaje_j2', 'estado', 'ganador', 'jugador_1']