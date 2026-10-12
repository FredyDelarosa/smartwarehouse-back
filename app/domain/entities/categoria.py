"""Entidad de dominio: Categoria."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(kw_only=True)
class Categoria:
    """Agrupa productos por tipo o familia."""

    nombre: str
    id: Optional[int] = None
    descripcion: Optional[str] = None
    activo: bool = True
    created_at: Optional[datetime] = None

    def validar(self) -> list[str]:
        """Validaciones básicas de la categoría."""
        errores: list[str] = []
        if not self.nombre or not self.nombre.strip():
            errores.append("El nombre de la categoría es obligatorio")
        if len(self.nombre) > 100:
            errores.append("El nombre no puede exceder 100 caracteres")
        return errores