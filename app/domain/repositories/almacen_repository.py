"""Puerto: AlmacenRepository."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities import Almacen


class AlmacenRepository(ABC):
    """Contrato de acceso a datos para almacenes."""

    @abstractmethod
    async def get_by_id(self, almacen_id: int) -> Optional[Almacen]: ...

    @abstractmethod
    async def list(self, *, solo_activos: bool = False) -> list[Almacen]: ...

    @abstractmethod
    async def create(self, almacen: Almacen) -> Almacen: ...

    @abstractmethod
    async def update(self, almacen: Almacen) -> Almacen: ...

    @abstractmethod
    async def delete(self, almacen_id: int) -> None: ...