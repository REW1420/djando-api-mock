"""
Respuestas estándar de la API.

Todas las vistas deben responder con la misma estructura (envelope) para que el
cliente (frontend, Postman, otra API) siempre sepa dónde buscar cada cosa:

    {
        "success": true | false,
        "message": "Texto legible para humanos",
        "data":    {...} | [...] | null,   # solo en respuestas exitosas
        "errors":  {...} | [...] | null    # solo en respuestas con error
    }

Se usa JsonResponse (y no rest_framework.Response) para que funcione tanto en
vistas normales de Django como en vistas con @api_view de DRF.
JsonResponse usa DjangoJSONEncoder, así que datetime, date, Decimal y UUID se
serializan sin problema.
"""
from http import HTTPStatus
from typing import Any

from django.http import JsonResponse


def api_response(
    *,
    success: bool,
    message: str = "",
    data: Any = None,
    errors: Any = None,
    status: int = HTTPStatus.OK,
) -> JsonResponse:
    """Construye la respuesta JSON con la estructura estándar de la API."""
    body = {
        "success": success,
        "message": message,
        "data": data,
        "errors": errors,
    }
    # safe=False permite que "data" sea una lista además de un dict
    # ensure_ascii=False: devuelve "ó" tal cual en vez de escaparlo como \uXXXX
    return JsonResponse(
        body,
        status=int(status),
        safe=False,
        json_dumps_params={"ensure_ascii": False},
    )


def success_response(
    data: Any = None,
    message: str = "Operación exitosa",
    status: int = HTTPStatus.OK,
) -> JsonResponse:
    """Respuesta exitosa (2xx)."""
    if not 200 <= int(status) < 300:
        raise ValueError(f"success_response requiere un status 2xx, se recibió {status}")
    return api_response(success=True, message=message, data=data, status=status)


def error_response(
    message: str,
    status: int = HTTPStatus.BAD_REQUEST,
    errors: Any = None,
) -> JsonResponse:
    """
    Respuesta de error (4xx / 5xx).

    `errors` es opcional y sirve para dar detalle, por ejemplo errores por campo:
        {"nombre": "Es obligatorio", "capacidad": "Debe ser positivo"}
    """
    if int(status) < 400:
        raise ValueError(f"error_response requiere un status 4xx o 5xx, se recibió {status}")
    return api_response(success=False, message=message, errors=errors, status=status)
