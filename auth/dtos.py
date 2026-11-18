"""
DTOs de la app "auth": objetos que transportan y validan los datos que llegan en
el body de las peticiones. NO son tablas de la base de datos (esas van en models.py).
"""
from dataclasses import dataclass


@dataclass
class LoginDTO:
    usuario: str
    contrasena: str

    def __post_init__(self):
        if not isinstance(self.usuario, str) or not self.usuario.strip():
            raise ValueError("El usuario es obligatorio")
        if not isinstance(self.contrasena, str) or not self.contrasena:
            raise ValueError("La contraseña es obligatoria")

        self.usuario = self.usuario.strip()


@dataclass
class RegisterDTO:
    username: str
    password: str

    def __post_init__(self):
        if not isinstance(self.username, str) or not self.username.strip():
            raise ValueError("El nombre de usuario es obligatorio")
        if not isinstance(self.password, str) or not self.password:
            raise ValueError("La contraseña es obligatoria")

        self.username = self.username.strip()
