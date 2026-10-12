"""Puerto: CategoriaRepository."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities import Categoria


class CategoriaRepository(ABC):
    """Contrato de acceso a datos para categorías."""

    @abstractmethod
    async def get_by_id(self, categoria_id: int) -> Optional[Categoria]: ...

    @abstractmethod
    async def get_by_nombre(self, nombre: str) -> Optional[Categoria]: ...

    @abstractmethod
    async def list(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        solo_activas: bool = True,
    ) -> list[Categoria]: ...

    @abstractmethod
    async def create(self, categoria: Categoria) -> Categoria: ...

    @abstractmethod
    async def update(self, categoria: Categoria) -> Categoria: ...

    @abstractmethod
    async def delete(self, categoria_id: int) -> None: ...