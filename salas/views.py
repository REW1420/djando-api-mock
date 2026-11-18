from http import HTTPStatus

from django.db import IntegrityError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from core.responses import success_response, error_response
from .serializers import SalaSerializer
from .service import list_salas, create_sala_service, get_sala_by_id, delete_sala_by_id


@api_view(['GET'])
@permission_classes([AllowAny])
def get_salas(request):
    salas = list_salas()
    # Una lista vacía NO es un error: se responde 200 con data = []
    # many=True: serializa una lista de objetos
    return success_response(
        SalaSerializer(salas, many=True).data,
        "Salas obtenidas exitosamente",
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def create_sala_view(request):
    # request.data: DRF ya convierte el body JSON en dict.
    # Si el JSON está mal formado, DRF lanza un error y core.exceptions lo formatea.
    serializer = SalaSerializer(data=request.data)
    if not serializer.is_valid():
        return error_response("Datos inválidos", HTTPStatus.BAD_REQUEST, serializer.errors)

    try:
        sala = create_sala_service(serializer.validated_data)
    except IntegrityError:
        return error_response("Ya existe una sala con ese nombre", HTTPStatus.CONFLICT)

    return success_response(
        SalaSerializer(sala).data,
        "Sala creada exitosamente",
        HTTPStatus.CREATED,
    )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_sala_view(request, sala_id):
    # sala_id llega desde la URL (ej. /salas/2 -> sala_id = 2)
    sala = get_sala_by_id(sala_id)
    if sala is None:
        return error_response(f"No existe una sala con id {sala_id}", HTTPStatus.NOT_FOUND)

    return success_response(SalaSerializer(sala).data, "Sala obtenida exitosamente")


@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_sala_view(request, sala_id):
    if not delete_sala_by_id(sala_id):
        return error_response(f"No existe una sala con id {sala_id}", HTTPStatus.NOT_FOUND)

    return success_response(message=f"Sala con id {sala_id} eliminada exitosamente")
