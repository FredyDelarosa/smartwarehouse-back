"""Entidad de dominio: Rol."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(kw_only=True)
class Rol:
    """
    Representa un rol del sistema.
    Valores esperados: 'Administrador', 'Supervisor', 'Almacenero'.
    """

    nombre: str
    id: Optional[int] = None
    descripcion: Optional[str] = None
    created_at: Optional[datetime] = None

    def es_administrador(self) -> bool:
        return self.nombre == "Administrador"

    def es_supervisor(self) -> bool:
        return self.nombre == "Supervisor"

    def es_almacenero(self) -> bool:
        return self.nombre == "Almacenero"