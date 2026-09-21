import os
import sys


def main():
    # Asigna las variables de entorno de desarrollo por defecto si no existen
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "config.settings.development",
    )
    os.environ.setdefault(
        "DJANGO_SECRET_KEY",
        "django-insecure-secret_key_de_prueba_para_desarrollo_local_12345",
    )
    os.environ.setdefault("DEBUG", "True")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No se pudo importar Django. "
            "Comprueba que Django esté instalado "
            "y que el entorno virtual esté activado."
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()