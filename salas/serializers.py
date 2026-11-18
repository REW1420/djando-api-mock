"""
SERIALIZERS de la app "salas".

Un serializer hace dos trabajos (reemplaza a to_dict() y al DTO):
    1. SALIDA:  objeto Sala      -> dict listo para JSON    (serializer.data)
    2. ENTRADA: JSON del cliente -> datos validados          (serializer.is_valid / validated_data)

ModelSerializer lee el modelo Sala y crea los campos solo, con sus reglas
(max_length=100, capacidad >= 1, etc.).
"""
from rest_framework import serializers

from .models import Sala


class SalaSerializer(serializers.ModelSerializer):
    # El JSONField del modelo acepta cualquier JSON; aquí exigimos una lista de textos.
    equipamiento = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False,
    )

    class Meta:
        model = Sala
        # Campos que se envían/reciben en la API (lo que no esté aquí, no sale)
        fields = ["id", "nombre", "capacidad", "equipamiento", "activa"]
        read_only_fields = ["id"]  # el cliente no puede mandar el id
        extra_kwargs = {
            # Quitamos el validador automático de "nombre único": la base de datos
            # ya lo garantiza y la vista responde 409 al capturar IntegrityError.
            # (Así también se cubre el caso de dos peticiones al mismo tiempo.)
            "nombre": {"validators": []},
        }

    # Nota: CharField ya quita espacios al inicio/final y rechaza el texto vacío.
    # Para reglas propias de un campo se agrega un método validate_<campo>(self, value).
