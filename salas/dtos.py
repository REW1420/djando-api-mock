

from dataclasses import dataclass


@dataclass
class CreateSalaDTO:
    nombre: str
    capacidad: int
    equipamiento: list[str]
    activa: bool = True

    def __post_init__(self):
        if not isinstance(self.nombre, str) or not self.nombre.strip():
            raise ValueError("El nombre de la sala es obligatorio")
      
        if not isinstance(self.capacidad, int) or self.capacidad <= 0:
            raise ValueError(
                "La capacidad de la sala es obligatoria y debe ser un número positivo")
        if not isinstance(self.equipamiento, list):
            raise ValueError("El equipamiento de la sala es obligatorio")
        if not isinstance(self.activa, bool):
            raise ValueError(
                "El estado de la sala es obligatorio y debe ser un booleano")
        self.nombre = self.nombre.strip()
       