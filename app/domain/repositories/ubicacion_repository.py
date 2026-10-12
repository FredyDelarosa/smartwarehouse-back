"""Puerto: UbicacionRepository."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities import Ubicacion


class UbicacionRepository(ABC):
    """Contrato de acceso a datos para ubicaciones físicas."""

    @abstractmethod
    async def get_by_id(self, ubicacion_id: int) -> Optional[Ubicacion]: ...

    @abstractmethod
    async def get_by_codigo(self, codigo: str) -> Optional[Ubicacion]:
        """Busca por código de ubicación, ej. 'P3-B-02'."""
        ...

    @abstractmethod
    async def get_by_qr(self, codigo_qr: str) -> Optional[Ubicacion]:
        """Busca por el contenido del código QR escaneado."""
        ...

    @abstractmethod
    async def list_by_almacen(
        self,
        almacen_id: int,
        *,
        solo_activas: bool = True,
    ) -> list[Ubicacion]: ...

    @abstractmethod
    async def list(self, *, skip: int = 0, limit: int = 100) -> list[Ubicacion]: ...

    @abstractmethod
    async def create(self, ubicacion: Ubicacion) -> Ubicacion: ...

    @abstractmethod
    async def update(self, ubicacion: Ubicacion) -> Ubicacion: ...

    @abstractmethod
    async def delete(self, ubicacion_id: int) -> None: ...