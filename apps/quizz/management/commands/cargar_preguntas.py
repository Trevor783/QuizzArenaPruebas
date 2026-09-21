import json
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.quizz.models import Quizz, Pregunta, Opcion

class Command(BaseCommand):
    help = 'Carga masiva de preguntas desde un fichero JSON externo para la API de Quizz'

    def add_arguments(self, parser):
        # Añadimos el argumento para indicar la ruta del archivo JSON desde la terminal
        parser.add_argument('json_file', type=str, help='Ruta al archivo JSON con las preguntas')

    def handle(self, *args, **options):
        archivo_path = options['json_file']

        try:
            with open(archivo_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Usamos transacciones atómicas para asegurar la integridad de la base de datos
            with transaction.atomic():
                # 1. Crear o recuperar el cuestionario principal
                quiz_data = data.get("quiz", {})
                quiz, _ = Quizz.objects.get_or_create(
                    titulo=quiz_data.get("titulo", "Evaluación General"),
                    defaults={"descripcion": quiz_data.get("descripcion", "")}
                )

                # 2. Recorrer el banco de preguntas del JSON
                banco_preguntas = data.get("preguntas", [])
                for item in banco_preguntas:
                    pregunta_texto = item.get("pregunta")
                    puntuacion = item.get("puntuacion", 10)

                    pregunta_obj, _ = Pregunta.objects.get_or_create(
                        quiz=quiz,
                        enunciado=pregunta_texto,
                        defaults={"puntuacion": puntuacion}
                    )

                    # 3. Crear las opciones asociadas
                    for op in item.get("opciones", []):
                        Opcion.objects.get_or_create(
                            pregunta=pregunta_obj,
                            texto=op.get("texto"),
                            defaults={"es_correcta": op.get("es_correcta", False)}
                        )

            self.stdout.write(self.style.SUCCESS(f"¡Preguntas cargadas con éxito desde '{archivo_path}'!"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error al procesar el archivo JSON: {e}"))