"""Puerto: ProductoRepository."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities import Producto


class ProductoRepository(ABC):
    """Contrato de acceso a datos para productos."""

    @abstractmethod
    async def get_by_id(self, producto_id: int) -> Optional[Producto]: ...

    @abstractmethod
    async def get_by_codigo(self, codigo: str) -> Optional[Producto]: ...

    @abstractmethod
    async def list(
        self,
        *,
        skip: int = 0,
        limit: int = 50,
        categoria_id: Optional[int] = None,
        solo_activos: bool = False,
    ) -> list[Producto]: ...

    @abstractmethod
    async def search(
        self,
        termino: str,
        *,
        limit: int = 20,
    ) -> list[Producto]:
        """
        Búsqueda por nombre o código.
        Es el corazón del caso de uso 'buscar producto'.
        """
        ...

    @abstractmethod
    async def count(
        self,
        *,
        categoria_id: Optional[int] = None,
        solo_activos: bool = False,
    ) -> int: ...

    @abstractmethod
    async def create(self, producto: Producto) -> Producto: ...

    @abstractmethod
    async def update(self, producto: Producto) -> Producto: ...

    @abstractmethod
    async def delete(self, producto_id: int) -> None: ...