"""Implementación: BusquedaRepository con SQLAlchemy async."""

from datetime import datetime
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import Busqueda
from app.domain.exceptions import BusquedaNoEncontradaError
from app.domain.repositories import BusquedaRepository
from app.infrastructure.database.models import BusquedaModel, ProductoModel
from app.infrastructure.repositories._mappers import (
    apply_busqueda,
    busqueda_to_entity,
)


class BusquedaRepositoryImpl(BusquedaRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, busqueda_id: int) -> Optional[Busqueda]:
        model = await self._session.get(BusquedaModel, busqueda_id)
        return busqueda_to_entity(model) if model else None

    async def list_by_usuario(
        self,
        usuario_id: int,
        *,
        skip: int = 0,
        limit: int = 50,
    ) -> list[Busqueda]:
        stmt = (
            select(BusquedaModel, ProductoModel.nombre)
            .outerjoin(ProductoModel, BusquedaModel.producto_id == ProductoModel.id)
            .where(BusquedaModel.usuario_id == usuario_id)
            .order_by(BusquedaModel.fecha_hora_inicio.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        busquedas = []
        for busqueda_model, producto_nombre in result.all():
            entity = busqueda_to_entity(busqueda_model)
            entity.producto_nombre = producto_nombre
            busquedas.append(entity)
        return busquedas

    async def list(
        self,
        *,
        desde: Optional[datetime] = None,
        hasta: Optional[datetime] = None,
        exito: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Busqueda]:
        stmt = select(BusquedaModel)
        if desde is not None:
            stmt = stmt.where(BusquedaModel.fecha_hora_inicio >= desde)
        if hasta is not None:
            stmt = stmt.where(BusquedaModel.fecha_hora_inicio <= hasta)
        if exito is not None:
            stmt = stmt.where(BusquedaModel.exito.is_(exito))
        stmt = (
            stmt.order_by(BusquedaModel.fecha_hora_inicio.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self._session.scalars(stmt)
        return [busqueda_to_entity(m) for m in result.all()]

    async def tiempo_promedio(
        self,
        *,
        desde: Optional[datetime] = None,
        hasta: Optional[datetime] = None,
    ) -> Optional[float]:
        stmt = select(func.avg(BusquedaModel.tiempo_busqueda_segundos)).where(
            BusquedaModel.tiempo_busqueda_segundos.is_not(None)
        )
        if desde is not None:
            stmt = stmt.where(BusquedaModel.fecha_hora_inicio >= desde)
        if hasta is not None:
            stmt = stmt.where(BusquedaModel.fecha_hora_inicio <= hasta)
        resultado = await self._session.scalar(stmt)
        return float(resultado) if resultado is not None else None

    async def count(
        self,
        *,
        desde: Optional[datetime] = None,
        hasta: Optional[datetime] = None,
        exito: Optional[bool] = None,
    ) -> int:
        stmt = select(func.count()).select_from(BusquedaModel)
        if desde is not None:
            stmt = stmt.where(BusquedaModel.fecha_hora_inicio >= desde)
        if hasta is not None:
            stmt = stmt.where(BusquedaModel.fecha_hora_inicio <= hasta)
        if exito is not None:
            stmt = stmt.where(BusquedaModel.exito.is_(exito))
        return int(await self._session.scalar(stmt) or 0)

    async def create(self, busqueda: Busqueda) -> Busqueda:
        model = BusquedaModel()
        apply_busqueda(busqueda, model)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return busqueda_to_entity(model)

    async def update(self, busqueda: Busqueda) -> Busqueda:
        if busqueda.id is None:
            raise ValueError("La búsqueda debe tener id para actualizarse")
        model = await self._session.get(BusquedaModel, busqueda.id)
        if model is None:
            raise BusquedaNoEncontradaError(details={"busqueda_id": busqueda.id})
        apply_busqueda(busqueda, model)
        await self._session.flush()
        await self._session.refresh(model)
        return busqueda_to_entity(model)