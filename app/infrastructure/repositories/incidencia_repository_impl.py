"""Implementación: IncidenciaRepository con SQLAlchemy async."""

from datetime import datetime
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import Incidencia, TipoIncidencia
from app.domain.exceptions import IncidenciaNoEncontradaError
from app.domain.repositories import IncidenciaRepository
from app.infrastructure.database.models import IncidenciaModel
from app.infrastructure.repositories._mappers import (
    apply_incidencia,
    incidencia_to_entity,
)


class IncidenciaRepositoryImpl(IncidenciaRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, incidencia_id: int) -> Optional[Incidencia]:
        model = await self._session.get(IncidenciaModel, incidencia_id)
        return incidencia_to_entity(model) if model else None

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
    ) -> list[Incidencia]:
        stmt = select(IncidenciaModel)
        if tipo is not None:
            stmt = stmt.where(IncidenciaModel.tipo == tipo)
        if resuelta is not None:
            stmt = stmt.where(IncidenciaModel.resuelta.is_(resuelta))
        if producto_id is not None:
            stmt = stmt.where(IncidenciaModel.producto_id == producto_id)
        if desde is not None:
            stmt = stmt.where(IncidenciaModel.fecha >= desde)
        if hasta is not None:
            stmt = stmt.where(IncidenciaModel.fecha <= hasta)
        stmt = stmt.order_by(IncidenciaModel.fecha.desc()).offset(skip).limit(limit)
        result = await self._session.scalars(stmt)
        return [incidencia_to_entity(m) for m in result.all()]

    async def count_by_tipo(
        self,
        tipo: TipoIncidencia,
        *,
        desde: Optional[datetime] = None,
        hasta: Optional[datetime] = None,
    ) -> int:
        stmt = (
            select(func.count())
            .select_from(IncidenciaModel)
            .where(IncidenciaModel.tipo == tipo)
        )
        if desde is not None:
            stmt = stmt.where(IncidenciaModel.fecha >= desde)
        if hasta is not None:
            stmt = stmt.where(IncidenciaModel.fecha <= hasta)
        return int(await self._session.scalar(stmt) or 0)

    async def create(self, incidencia: Incidencia) -> Incidencia:
        model = IncidenciaModel()
        apply_incidencia(incidencia, model)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return incidencia_to_entity(model)

    async def update(self, incidencia: Incidencia) -> Incidencia:
        if incidencia.id is None:
            raise ValueError("La incidencia debe tener id para actualizarse")
        model = await self._session.get(IncidenciaModel, incidencia.id)
        if model is None:
            raise IncidenciaNoEncontradaError(
                details={"incidencia_id": incidencia.id}
            )
        apply_incidencia(incidencia, model)
        await self._session.flush()
        await self._session.refresh(model)
        return incidencia_to_entity(model)