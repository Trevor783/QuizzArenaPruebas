from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    QuizzViewSet, 
    PreguntaListAPIView, 
    ListaQuizzesView, 
    PerfilJugadorViewSet, 
    Partida1v1ViewSet
)

router = DefaultRouter()
router.register(r'quizzes', QuizzViewSet, basename='quizz')
router.register(r'perfiles', PerfilJugadorViewSet, basename='perfil')
router.register(r'partidas-1v1', Partida1v1ViewSet, basename='partida-1v1')

urlpatterns = [
    path('web/', ListaQuizzesView.as_view(), name='lista_quizzes_web'),
    path('preguntas/', PreguntaListAPIView.as_view(), name='lista_preguntas_api'),
    path('', include(router.urls)),
]