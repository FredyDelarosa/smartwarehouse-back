"""
Base declarativa de SQLAlchemy 2.0.

Todos los modelos ORM heredan de `Base`. En este archivo también
importamos todos los modelos para que `Base.metadata` quede completo
(necesario para Alembic y para `create_all`).
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Clase base declarativa para todos los modelos ORM."""
    pass


# El import de los modelos se hace al final del paquete
# (ver `app.infrastructure.database.models.__init__`).
# Se importan aquí para que Alembic los descubra al cargar `Base.metadata`.
from app.infrastructure.database import models  # noqa: E402,F401