import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.conf import settings
from apps.quizz.models import Quizz, Pregunta, Opcion

class Command(BaseCommand):
    help = 'Carga masiva de preguntas desde un fichero JSON externo para la API de Quizz'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Ruta al archivo JSON con las preguntas')

    def handle(self, *args, **options):
        archivo_entrada = Path(options['json_file'])
        if not archivo_entrada.is_absolute():
            rutas_posibles = [
                Path.cwd() / archivo_entrada,
                settings.BASE_DIR / archivo_entrada,
                settings.BASE_DIR.parent / archivo_entrada,
            ]
            archivo_path = next((ruta for ruta in rutas_posibles if ruta.is_file()), rutas_posibles[0])
        else:
            archivo_path = archivo_entrada

        if not archivo_path.is_file():
            raise CommandError(f"No existe el archivo JSON: {archivo_path}")

        try:
            with archivo_path.open('r', encoding='utf-8') as archivo:
                data = json.load(archivo)
        except json.JSONDecodeError as error:
            raise CommandError(
                f"El JSON no es válido en la línea {error.lineno}, columna {error.colno}: {error.msg}"
            ) from error

        if not isinstance(data, dict):
            raise CommandError("El JSON debe contener un objeto con 'quizz' y 'preguntas'.")

        quizz_data = data.get("quizz", {})
        banco_preguntas = data.get("preguntas", [])
        if not isinstance(quizz_data, dict) or not isinstance(banco_preguntas, list):
            raise CommandError("'quizz' debe ser un objeto y 'preguntas' debe ser una lista.")

        titulo = quizz_data.get("titulo", "Evaluación General")
        if not titulo:
            raise CommandError("El campo 'quizz.titulo' no puede estar vacío.")

        with transaction.atomic():
            quizz, _ = Quizz.objects.update_or_create(
                titulo=titulo,
                defaults={"descripcion": quizz_data.get("descripcion", "")},
            )

            preguntas_cargadas = 0
            opciones_cargadas = 0
            for indice, item in enumerate(banco_preguntas, start=1):
                if not isinstance(item, dict) or not item.get("pregunta"):
                    raise CommandError(f"La pregunta número {indice} no tiene el campo 'pregunta'.")

                pregunta_obj, _ = Pregunta.objects.update_or_create(
                    quizz=quizz,
                    texto=item["pregunta"],
                )
                preguntas_cargadas += 1

                opciones = item.get("opciones", [])
                if not isinstance(opciones, list) or not opciones:
                    raise CommandError(f"La pregunta número {indice} debe tener opciones.")

                for opcion in opciones:
                    if not isinstance(opcion, dict) or not opcion.get("texto"):
                        raise CommandError(f"Una opción de la pregunta número {indice} no tiene texto.")
                    Opcion.objects.update_or_create(
                        pregunta=pregunta_obj,
                        texto=opcion["texto"],
                        defaults={"es_correcta": bool(opcion.get("es_correcta", False))},
                    )
                    opciones_cargadas += 1

        self.stdout.write(self.style.SUCCESS(
            f"Quizz cargado desde '{archivo_path}': {preguntas_cargadas} preguntas y "
            f"{opciones_cargadas} opciones."
        ))