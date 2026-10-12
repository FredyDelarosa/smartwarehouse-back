"""Puerto: IncidenciaRepository."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from app.domain.entities import Incidencia, TipoIncidencia


class IncidenciaRepository(ABC):
    """Contrato de acceso a datos para incidencias del almacén."""

    @abstractmethod
    async def get_by_id(self, incidencia_id: int) -> Optional[Incidencia]: ...

    @abstractmethod
    async def list(
        self,
        *,
        tipo: Optional[TipoIncidencia] = None,
        resuelta: Optional[bool] = None,
        producto_id: Optional[int] = None,
        desde: Optional[datetime] = None,
        hasta: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Incidencia]: ...

    @abstractmethod
    async def count_by_tipo(
        self,
        tipo: TipoIncidencia,
        *,
        desde: Optional[datetime] = None,
        hasta: Optional[datetime] = None,
    ) -> int: ...

    @abstractmethod
    async def create(self, incidencia: Incidencia) -> Incidencia: ...

    @abstractmethod
    async def update(self, incidencia: Incidencia) -> Incidencia: ...