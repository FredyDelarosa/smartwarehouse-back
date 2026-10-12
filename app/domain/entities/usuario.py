"""Entidad de dominio: Usuario."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.domain.entities.rol import Rol


@dataclass(kw_only=True)
class Usuario:
    """
    Representa a una persona que usa el sistema.

    Nota: `password_hash` se mantiene aquí porque es parte del estado
    que la infraestructura necesita persistir. La capa de aplicación
    nunca debe exponerlo en respuestas.
    """

    nombre: str
    email: str
    password_hash: str
    rol_id: int
    id: Optional[int] = None
    activo: bool = True
    fecha_creacion: Optional[datetime] = None
    ultimo_acceso: Optional[datetime] = None

    # Relación opcional (se rellena si el repositorio la trae)
    rol: Optional[Rol] = None

    def puede_autenticarse(self) -> bool:
        """Un usuario puede autenticarse solo si está activo."""
        return self.activo

    def marcar_acceso(self, momento: Optional[datetime] = None) -> None:
        """Registra el último acceso del usuario."""
        self.ultimo_acceso = momento or datetime.now(tz=None)

    @property
    def nombre_rol(self) -> Optional[str]:
        return self.rol.nombre if self.rol else None