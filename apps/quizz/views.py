from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views.generic import ListView
from .models import Quizz, Pregunta, Opcion, Partida1v1, PerfilJugador
from .serializers import (
    QuizzSerializer, 
    PreguntaSerializer, 
    PerfilJugadorSerializer, 
    Partida1v1Serializer
)

class QuizzViewSet(viewsets.ModelViewSet):
    queryset = Quizz.objects.all()
    serializer_class = QuizzSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PreguntaListAPIView(generics.ListCreateAPIView):
    queryset = Pregunta.objects.all()
    serializer_class = PreguntaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ListaQuizzesView(ListView):
    model = Quizz
    template_name = 'quizz/lista_quizzes.html'
    context_object_name = 'quizzes'

    def get_queryset(self):
        return Quizz.objects.prefetch_related('preguntas__opciones').all()


class PerfilJugadorViewSet(viewsets.ModelViewSet):
    queryset = PerfilJugador.objects.all()
    serializer_class = PerfilJugadorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class Partida1v1ViewSet(viewsets.ModelViewSet):
    queryset = Partida1v1.objects.all()
    serializer_class = Partida1v1Serializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(jugador_1=self.request.user)

    @action(detail=True, methods=['post'])
    def unirse(self, request, pk=None):
        partida = self.get_object()
        
        if partida.jugador_2 is not None:
            return Response(
                {"error": "La sala ya está llena."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if partida.jugador_1 == request.user:
            return Response(
                {"error": "No puedes unirte a tu propia partida como oponente."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        partida.jugador_2 = request.user
        partida.estado = 'en_curso'
        partida.save()
        
        serializer = self.get_serializer(partida)
        return Response(serializer.data)