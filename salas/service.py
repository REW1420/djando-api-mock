from .models import Sala


def list_salas():
    return Sala.objects.all()


def create_sala_service(datos: dict):
    # "datos" es serializer.validated_data: ya viene validado y limpio
    return Sala.objects.create(**datos)


def get_sala_by_id(sala_id: int):
    # .filter().first() devuelve None si no existe (en vez de lanzar excepción como .get())
    return Sala.objects.filter(id=sala_id).first()


def delete_sala_by_id(sala_id: int):
    sala = Sala.objects.filter(id=sala_id).first()
    if sala is None:
        return False
    sala.delete()
    return True
