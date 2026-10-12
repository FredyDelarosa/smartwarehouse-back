"""Puerto: InventarioRepository."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities import Inventario, Producto


class InventarioRepository(ABC):
    """Contrato de acceso a datos para el stock por ubicación."""

    @abstractmethod
    async def get_by_id(self, inventario_id: int) -> Optional[Inventario]: ...

    @abstractmethod
    async def get_by_producto_y_ubicacion(
        self, producto_id: int, ubicacion_id: int
    ) -> Optional[Inventario]: ...

    @abstractmethod
    async def list_by_producto(
        self, producto_id: int
    ) -> list[Inventario]: ...

    @abstractmethod
    async def list_by_ubicacion(
        self, ubicacion_id: int
    ) -> list[Inventario]: ...

    @abstractmethod
    async def stock_total_producto(self, producto_id: int) -> int:
        """Suma la cantidad de un producto en todas sus ubicaciones."""
        ...

    @abstractmethod
    async def list_stock_bajo(self) -> list[tuple[Producto, int]]:
        """
        Devuelve tuplas (Producto, stock_total) para productos cuyo
        stock total es menor que su stock_minimo.
        """
        ...

    @abstractmethod
    async def create(self, inventario: Inventario) -> Inventario: ...

    @abstractmethod
    async def update(self, inventario: Inventario) -> Inventario: ...

    @abstractmethod
    async def upsert(
        self,
        producto_id: int,
        ubicacion_id: int,
        delta_cantidad: int,
    ) -> Inventario:
        """
        Crea el registro si no existe e incrementa/decrementa `delta_cantidad`.
        Se usará al registrar movimientos de entrada/salida/traslado.
        """
        ...

    @abstractmethod
    async def delete(self, inventario_id: int) -> None: ...