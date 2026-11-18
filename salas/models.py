"""
MODELOS de la app "salas": las tablas de la base de datos.

Después de crear o cambiar un modelo:
    python manage.py makemigrations   -> genera el archivo de migración en salas/migrations/
    python manage.py migrate          -> aplica la migración en PostgreSQL
"""
from django.core.validators import MinValueValidator
from django.db import models


class Sala(models.Model):
    # id: Django lo crea solo (autoincremental, llave primaria)

    nombre = models.CharField(max_length=100, unique=True)

    # Validador: lo revisa Django (formularios, full_clean, admin).
    # CheckConstraint (abajo): lo garantiza la propia base de datos.
    capacidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    # Lista de equipos, ej. ["proyector", "pizarra"]. Se guarda como JSON en Postgres.
    equipamiento = models.JSONField(default=list, blank=True)

    activa = models.BooleanField(default=True)

    class Meta:
        db_table = "salas"
        ordering = ["nombre"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(capacidad__gt=0),
                name="sala_capacidad_mayor_a_0",
            ),
        ]

    def __str__(self):
        return self.nombre

