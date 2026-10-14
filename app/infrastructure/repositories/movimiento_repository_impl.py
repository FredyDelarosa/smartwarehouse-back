"""Implementación: MovimientoRepository con SQLAlchemy async."""

from datetime import datetime
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import Movimiento, TipoMovimiento
from app.domain.repositories import MovimientoRepository
from app.infrastructure.database.models import (
    MovimientoModel,
    UsuarioModel,
)
from app.infrastructure.repositories._mappers import (
    apply_movimiento,
    movimiento_to_entity,
)


class MovimientoRepositoryImpl(MovimientoRepository):
    def __init__(self, session: AsyncSession, *, almacen_id: int | None = None) -> None:
        self._session = session
        # Multialmacén: un movimiento pertenece al almacén de quien lo registra.
        # Se usa `usuario_id` y no la ubicación porque un movimiento es un
        # HECHO del almacén (entró, salió, se trasladó), no una propiedad del
        # estante: aunque las referencias de ubicación ya están acotadas, el
        # autor es quien define a qué almacén pertenece el registro.
        self._almacen_id = almacen_id

    def _acotar(self, stmt):
        if self._almacen_id is None:
            return stmt
        return stmt.join(
            UsuarioModel, UsuarioModel.id == MovimientoModel.usuario_id
        ).where(UsuarioModel.almacen_id == self._almacen_id)

    async def get_by_id(self, movimiento_id: int) -> Optional[Movimiento]:
        stmt = self._acotar(select(MovimientoModel)).where(
            MovimientoModel.id == movimiento_id
        )
        model = await self._session.scalar(stmt)
        return movimiento_to_entity(model) if model else None

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
    ) -> list[Movimiento]:
        stmt = self._acotar(select(MovimientoModel))
        if producto_id is not None:
            stmt = stmt.where(MovimientoModel.producto_id == producto_id)
        if ubicacion_id is not None:
            stmt = stmt.where(
                (MovimientoModel.ubicacion_origen_id == ubicacion_id)
                | (MovimientoModel.ubicacion_destino_id == ubicacion_id)
            )
        if usuario_id is not None:
            stmt = stmt.where(MovimientoModel.usuario_id == usuario_id)
        if tipo is not None:
            stmt = stmt.where(MovimientoModel.tipo == tipo)
        if desde is not None:
            stmt = stmt.where(MovimientoModel.fecha >= desde)
        if hasta is not None:
            stmt = stmt.where(MovimientoModel.fecha <= hasta)
        stmt = stmt.order_by(MovimientoModel.fecha.desc()).offset(skip).limit(limit)
        result = await self._session.scalars(stmt)
        return [movimiento_to_entity(m) for m in result.all()]

    async def count_by_tipo(
        self,
        tipo: TipoMovimiento,
        *,
        desde: Optional[datetime] = None,
        hasta: Optional[datetime] = None,
    ) -> int:
        stmt = self._acotar(
            select(func.count()).select_from(MovimientoModel)
        ).where(MovimientoModel.tipo == tipo)
        if desde is not None:
            stmt = stmt.where(MovimientoModel.fecha >= desde)
        if hasta is not None:
            stmt = stmt.where(MovimientoModel.fecha <= hasta)
        return int(await self._session.scalar(stmt) or 0)

    async def create(self, movimiento: Movimiento) -> Movimiento:
        model = MovimientoModel()
        apply_movimiento(movimiento, model)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return movimiento_to_entity(model)