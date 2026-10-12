"""Implementación: AlmacenRepository con SQLAlchemy async."""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import Almacen
from app.domain.exceptions import EntidadNoEncontradaError
from app.domain.repositories import AlmacenRepository
from app.infrastructure.database.models import AlmacenModel
from app.infrastructure.repositories._mappers import (
    almacen_to_entity,
    apply_almacen,
)


class AlmacenRepositoryImpl(AlmacenRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, almacen_id: int) -> Optional[Almacen]:
        model = await self._session.get(AlmacenModel, almacen_id)
        return almacen_to_entity(model) if model else None

    async def list(self, *, solo_activos: bool = False) -> list[Almacen]:
        stmt = select(AlmacenModel)
        if solo_activos:
            stmt = stmt.where(AlmacenModel.activo.is_(True))
        stmt = stmt.order_by(AlmacenModel.id)
        result = await self._session.scalars(stmt)
        return [almacen_to_entity(m) for m in result.all()]

    async def create(self, almacen: Almacen) -> Almacen:
        model = AlmacenModel()
        apply_almacen(almacen, model)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return almacen_to_entity(model)

    async def update(self, almacen: Almacen) -> Almacen:
        if almacen.id is None:
            raise ValueError("El almacén debe tener id para actualizarse")
        model = await self._session.get(AlmacenModel, almacen.id)
        if model is None:
            raise EntidadNoEncontradaError(
                "Almacén no encontrado", details={"almacen_id": almacen.id}
            )
        apply_almacen(almacen, model)
        await self._session.flush()
        await self._session.refresh(model)
        return almacen_to_entity(model)

    async def delete(self, almacen_id: int) -> None:
        model = await self._session.get(AlmacenModel, almacen_id)
        if model is None:
            raise EntidadNoEncontradaError(
                "Almacén no encontrado", details={"almacen_id": almacen_id}
            )
        await self._session.delete(model)
        await self._session.flush()