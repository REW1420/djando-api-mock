"""
Manejador global de errores de DRF.

Hay errores que DRF responde solo, antes de llegar a tu código:
    - JSON mal formado          -> 400
    - Token faltante/inválido   -> 401
    - Sin permisos              -> 403
    - Método no permitido       -> 405
Por defecto vienen como {"detail": "..."}. Este manejador los convierte a la
misma estructura estándar de core.responses, para que TODA la API sea igual.

Se activa en config/settings.py -> REST_FRAMEWORK["EXCEPTION_HANDLER"].
"""
from rest_framework.views import exception_handler


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        # Error no controlado (bug): Django responde 500 y lo registra en el log
        return None

    data = response.data
    if isinstance(data, dict) and "detail" in data:
        # Errores simples: {"detail": "Authentication credentials were not provided."}
        message, errors = str(data["detail"]), None
    else:
        # Errores de validación lanzados con raise_exception=True: detalle por campo
        message, errors = "Datos inválidos", data

    # Se modifica la Response de DRF (en vez de crear una nueva) para conservar
    # sus headers, ej. WWW-Authenticate en los 401.
    response.data = {
        "success": False,
        "message": message,
        "data": None,
        "errors": errors,
    }
    return response
