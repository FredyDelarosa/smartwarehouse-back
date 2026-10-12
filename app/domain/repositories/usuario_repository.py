"""Puerto: UsuarioRepository."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from app.domain.entities import Usuario


class UsuarioRepository(ABC):
    """Contrato de acceso a datos para usuarios."""

    @abstractmethod
    async def get_by_id(self, usuario_id: int) -> Optional[Usuario]: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[Usuario]: ...

    @abstractmethod
    async def list(self, *, solo_activos: bool = False) -> list[Usuario]: ...

    @abstractmethod
    async def create(self, usuario: Usuario) -> Usuario: ...

    @abstractmethod
    async def update(self, usuario: Usuario) -> Usuario: ...

    @abstractmethod
    async def delete(self, usuario_id: int) -> None: ...

    @abstractmethod
    async def marcar_acceso(
        self, usuario_id: int, momento: datetime
    ) -> None: ...