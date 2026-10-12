"""Entidad de dominio: Almacen."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(kw_only=True)
class Almacen:
    """Representa un almacén físico."""

    nombre: str
    id: Optional[int] = None
    direccion: Optional[str] = None
    activo: bool = True
    created_at: Optional[datetime] = None

    def esta_activo(self) -> bool:
        return self.activo