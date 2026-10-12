"""Implementación: RolRepository con SQLAlchemy async."""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import Rol
from app.domain.repositories import RolRepository
from app.infrastructure.database.models import RolModel
from app.infrastructure.repositories._mappers import apply_rol, rol_to_entity


class RolRepositoryImpl(RolRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, rol_id: int) -> Optional[Rol]:
        model = await self._session.get(RolModel, rol_id)
        return rol_to_entity(model) if model else None

    async def get_by_nombre(self, nombre: str) -> Optional[Rol]:
        stmt = select(RolModel).where(RolModel.nombre == nombre)
        model = await self._session.scalar(stmt)
        return rol_to_entity(model) if model else None

    async def list(self) -> list[Rol]:
        stmt = select(RolModel).order_by(RolModel.id)
        result = await self._session.scalars(stmt)
        return [rol_to_entity(m) for m in result.all()]

    async def create(self, rol: Rol) -> Rol:
        model = RolModel()
        apply_rol(rol, model)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return rol_to_entity(model)