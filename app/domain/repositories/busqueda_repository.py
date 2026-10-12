"""Puerto: BusquedaRepository."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from app.domain.entities import Busqueda


class BusquedaRepository(ABC):
    """Contrato de acceso a datos para las búsquedas de producto."""

    @abstractmethod
    async def get_by_id(self, busqueda_id: int) -> Optional[Busqueda]: ...

    @abstractmethod
    async def list_by_usuario(
        self,
        usuario_id: int,
        *,
        skip: int = 0,
        limit: int = 50,
    ) -> list[Busqueda]: ...

    @abstractmethod
    async def list(
        self,
        *,
        desde: Optional[datetime] = None,
        hasta: Optional[datetime] = None,
        exito: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Busqueda]: ...

    @abstractmethod
    async def tiempo_promedio(
        self,
        *,
        desde: Optional[datetime] = None,
        hasta: Optional[datetime] = None,
    ) -> Optional[float]:
        """
        Promedio de tiempo de búsqueda en segundos.
        Devuelve None si no hay búsquedas finalizadas en el rango.
        """
        ...

    @abstractmethod
    async def count(
        self,
        *,
        desde: Optional[datetime] = None,
        hasta: Optional[datetime] = None,
        exito: Optional[bool] = None,
    ) -> int: ...

    @abstractmethod
    async def create(self, busqueda: Busqueda) -> Busqueda: ...

    @abstractmethod
    async def update(self, busqueda: Busqueda) -> Busqueda: ...