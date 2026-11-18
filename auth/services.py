from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


def validate_login(username, password):
    """Devuelve el usuario si las credenciales son correctas, o None si no.

    authenticate() busca el usuario en la base de datos y compara la
    contraseña contra el hash guardado.
    """
    return authenticate(username=username, password=password)


def generate_tokens(user):
    """Genera el par de tokens JWT (refresh y access) para un usuario."""
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def register_user(username, password):
    """Crea un usuario nuevo. Lanza ValueError si el nombre ya existe.

    create_user() guarda la contraseña hasheada, nunca en texto plano.
    """
    if User.objects.filter(username=username).exists():
        raise ValueError("El nombre de usuario ya existe")

    user = User.objects.create_user(username=username, password=password)
    return {"id": user.id, "username": user.username}
