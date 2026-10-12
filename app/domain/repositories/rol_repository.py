"""Puerto: RolRepository."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities import Rol


class RolRepository(ABC):
    """Contrato de acceso a datos para roles."""

    @abstractmethod
    async def get_by_id(self, rol_id: int) -> Optional[Rol]: ...

    @abstractmethod
    async def get_by_nombre(self, nombre: str) -> Optional[Rol]: ...

    @abstractmethod
    async def list(self) -> list[Rol]: ...

    @abstractmethod
    async def create(self, rol: Rol) -> Rol: ...