"""
LÓGICA DE NEGOCIO DE LA APP "health" (equivale a services/ en Express).

Django no crea este archivo; lo agregamos para separar responsabilidades.

Estas funciones NO deben recibir `request` ni devolver respuestas HTTP.
Reciben datos normales y devuelven datos normales, así se pueden reusar
desde vistas, comandos o tests.
"""
# from .models import Usuario


def get_status():
    """Devuelve el estado de la aplicación.

    """
    return True
