from django.db import models
from django.contrib.auth.models import User

class PerfilJugador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    puntos_experiencia = models.PositiveIntegerField(default=0)
    victorias_1v1 = models.PositiveIntegerField(default=0)
    derrotas_1v1 = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Jugador: {self.user.username} (XP: {self.puntos_experiencia})"


class Quizz(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class Pregunta(models.Model):
    quizz = models.ForeignKey(Quizz, related_name='preguntas', on_delete=models.CASCADE)
    texto = models.TextField()

    def __str__(self):
        return self.texto


class Opcion(models.Model):
    pregunta = models.ForeignKey(Pregunta, related_name='opciones', on_delete=models.CASCADE)
    texto = models.CharField(max_length=255)
    es_correcta = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.texto} ({'Correcta' if self.es_correcta else 'Incorrecta'})"


class Partida1v1(models.Model):
    ESTADOS_PARTIDA = [
        ('esperando', 'Esperando Oponente'),
        ('en_curso', 'En Curso'),
        ('finalizado', 'Finalizado'),
    ]

    quizz = models.ForeignKey(Quizz, on_delete=models.CASCADE)
    jugador_1 = models.ForeignKey(User, related_name='partidas_como_j1', on_delete=models.CASCADE)
    jugador_2 = models.ForeignKey(User, related_name='partidas_como_j2', null=True, blank=True, on_delete=models.SET_NULL)
    
    puntaje_j1 = models.IntegerField(default=0)
    puntaje_j2 = models.IntegerField(default=0)
    
    estado = models.CharField(max_length=20, choices=ESTADOS_PARTIDA, default='esperando')
    ganador = models.ForeignKey(User, related_name='duelos_ganados', null=True, blank=True, on_delete=models.SET_NULL)
    
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        j2_nombre = self.jugador_2.username if self.jugador_2 else "Esperando..."
        return f"Duelo: {self.jugador_1.username} vs {j2_nombre} [{self.get_estado_display()}]"