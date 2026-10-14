"""Implementación: IncidenciaRepository con SQLAlchemy async."""

from datetime import datetime
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import Incidencia, TipoIncidencia
from app.domain.exceptions import IncidenciaNoEncontradaError
from app.domain.repositories import IncidenciaRepository
from app.infrastructure.database.models import (
    IncidenciaModel,
    UsuarioModel,
)
from app.infrastructure.repositories._mappers import (
    apply_incidencia,
    incidencia_to_entity,
)


class IncidenciaRepositoryImpl(IncidenciaRepository):
    def __init__(self, session: AsyncSession, *, almacen_id: int | None = None) -> None:
        self._session = session
        # Multialmacén: una incidencia la reporta un usuario de un almacén, y
        # pertenece a ese almacén. Puede no tener producto ni ubicación (p. ej.
        # "fuga de agua en el pasillo"), así que el almacén se toma siempre del
        # autor, nunca del objeto tratado.
        self._almacen_id = almacen_id

    def _acotar(self, stmt):
        if self._almacen_id is None:
            return stmt
        return stmt.join(
            UsuarioModel, UsuarioModel.id == IncidenciaModel.usuario_id
        ).where(UsuarioModel.almacen_id == self._almacen_id)

    async def get_by_id(self, incidencia_id: int) -> Optional[Incidencia]:
        stmt = self._acotar(select(IncidenciaModel)).where(
            IncidenciaModel.id == incidencia_id
        )
        model = await self._session.scalar(stmt)
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
        stmt = self._acotar(select(IncidenciaModel))
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
        stmt = self._acotar(
            select(func.count()).select_from(IncidenciaModel)
        ).where(IncidenciaModel.tipo == tipo)
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
        stmt = self._acotar(select(IncidenciaModel)).where(
            IncidenciaModel.id == incidencia.id
        )
        model = await self._session.scalar(stmt)
        if model is None:
            raise IncidenciaNoEncontradaError(
                details={"incidencia_id": incidencia.id}
            )
        apply_incidencia(incidencia, model)
        await self._session.flush()
        await self._session.refresh(model)
        return incidencia_to_entity(model)