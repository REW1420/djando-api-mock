import json
from .dtos import LoginDTO, RegisterDTO
from .services import validate_login, register_user, generate_tokens
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST,require_GET

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@csrf_exempt
@require_POST
def login(request):
    # Leer el body (JSON) que manda el cliente
    try:
        body = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "El body no es un JSON válido"}, status=400)

    # El body tiene que ser un objeto JSON {...}, no una lista ni un texto
    if not isinstance(body, dict):
        return JsonResponse({"error": "El body debe ser un objeto JSON"}, status=400)

    # Validar los parámetros con el DTO (usuario y contraseña obligatorios)
    try:
        dto = LoginDTO(body.get("username"), body.get("password"))
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

    user = validate_login(dto.usuario, dto.contrasena)
    if user is None:
        return JsonResponse({"error": "Usuario o contraseña incorrectos"}, status=401)

    return JsonResponse(generate_tokens(user))

@csrf_exempt
@require_POST
def register(request):
    # Leer el body (JSON) que manda el cliente
    try:
        body = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "El body no es un JSON válido"}, status=400)

    # El body tiene que ser un objeto JSON {...}, no una lista ni un texto
    if not isinstance(body, dict):
        return JsonResponse({"error": "El body debe ser un objeto JSON"}, status=400)

    # Validar los parámetros con el DTO (usuario y contraseña obligatorios)
    try:
        dto = RegisterDTO(body.get("username"), body.get("password"))
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

    try:
        user_data = register_user(dto.username, dto.password)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"usuario": user_data}, status=201)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_me(request):
    return Response({"message": "¡Hola desde la vista de auth!", "usuario": request.user.username})