"""Implementación: UbicacionRepository con SQLAlchemy async."""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import Ubicacion
from app.domain.exceptions import UbicacionNoEncontradaError
from app.domain.repositories import UbicacionRepository
from app.infrastructure.database.models import UbicacionModel
from app.infrastructure.repositories._mappers import (
    apply_ubicacion,
    ubicacion_to_entity,
)


class UbicacionRepositoryImpl(UbicacionRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, ubicacion_id: int) -> Optional[Ubicacion]:
        model = await self._session.get(UbicacionModel, ubicacion_id)
        return ubicacion_to_entity(model) if model else None

    async def get_by_codigo(self, codigo: str) -> Optional[Ubicacion]:
        stmt = select(UbicacionModel).where(
            UbicacionModel.codigo_ubicacion == codigo.strip().upper()
        )
        model = await self._session.scalar(stmt)
        return ubicacion_to_entity(model) if model else None

    async def get_by_qr(self, codigo_qr: str) -> Optional[Ubicacion]:
        stmt = select(UbicacionModel).where(UbicacionModel.codigo_qr == codigo_qr)
        model = await self._session.scalar(stmt)
        return ubicacion_to_entity(model) if model else None

    async def list_by_almacen(
        self, almacen_id: int, *, solo_activas: bool = True
    ) -> list[Ubicacion]:
        stmt = select(UbicacionModel).where(UbicacionModel.almacen_id == almacen_id)
        if solo_activas:
            stmt = stmt.where(UbicacionModel.activo.is_(True))
        stmt = stmt.order_by(
            UbicacionModel.pasillo, UbicacionModel.estante, UbicacionModel.nivel
        )
        result = await self._session.scalars(stmt)
        return [ubicacion_to_entity(m) for m in result.all()]

    async def list(self, *, skip: int = 0, limit: int = 100) -> list[Ubicacion]:
        stmt = (
            select(UbicacionModel)
            .order_by(
                UbicacionModel.pasillo, UbicacionModel.estante, UbicacionModel.nivel
            )
            .offset(skip)
            .limit(limit)
        )
        result = await self._session.scalars(stmt)
        return [ubicacion_to_entity(m) for m in result.all()]

    async def create(self, ubicacion: Ubicacion) -> Ubicacion:
        model = UbicacionModel()
        apply_ubicacion(ubicacion, model)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return ubicacion_to_entity(model)

    async def update(self, ubicacion: Ubicacion) -> Ubicacion:
        if ubicacion.id is None:
            raise ValueError("La ubicación debe tener id para actualizarse")
        model = await self._session.get(UbicacionModel, ubicacion.id)
        if model is None:
            raise UbicacionNoEncontradaError(
                details={"ubicacion_id": ubicacion.id}
            )
        apply_ubicacion(ubicacion, model)
        await self._session.flush()
        await self._session.refresh(model)
        return ubicacion_to_entity(model)

    async def delete(self, ubicacion_id: int) -> None:
        model = await self._session.get(UbicacionModel, ubicacion_id)
        if model is None:
            raise UbicacionNoEncontradaError(details={"ubicacion_id": ubicacion_id})
        await self._session.delete(model)
        await self._session.flush()