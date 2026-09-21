from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Quizz, Pregunta, Opcion, PerfilJugador, Partida1v1

class OpcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opcion
        fields = ['id', 'texto', 'es_correcta']


class PreguntaSerializer(serializers.ModelSerializer):
    opciones = OpcionSerializer(many=True, read_only=True)

    class Meta:
        model = Pregunta
        fields = ['id', 'texto', 'opciones']


class QuizzSerializer(serializers.ModelSerializer):
    preguntas = PreguntaSerializer(many=True, read_only=True)

    class Meta:
        model = Quizz
        fields = ['id', 'titulo', 'descripcion', 'creado_en', 'preguntas']


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