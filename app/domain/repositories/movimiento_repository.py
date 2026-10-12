"""Puerto: MovimientoRepository."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from app.domain.entities import Movimiento, TipoMovimiento


class MovimientoRepository(ABC):
    """Contrato de acceso a datos para movimientos de inventario."""

    @abstractmethod
    async def get_by_id(self, movimiento_id: int) -> Optional[Movimiento]: ...

    @abstractmethod
    async def list(
        self,
        *,
        producto_id: Optional[int] = None,
        ubicacion_id: Optional[int] = None,
        usuario_id: Optional[int] = None,
        tipo: Optional[TipoMovimiento] = None,
        desde: Optional[datetime] = None,
        hasta: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Movimiento]: ...

    @abstractmethod
    async def count_by_tipo(
        self,
        tipo: TipoMovimiento,
        *,
        desde: Optional[datetime] = None,
        hasta: Optional[datetime] = None,
    ) -> int: ...

    @abstractmethod
    async def create(self, movimiento: Movimiento) -> Movimiento: ...