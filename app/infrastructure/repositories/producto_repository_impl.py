"""Implementación: ProductoRepository con SQLAlchemy async."""
from __future__ import annotations
from typing import Optional

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import Producto
from app.domain.exceptions import ProductoNoEncontradoError
from app.domain.repositories import ProductoRepository
from app.infrastructure.database.models import ProductoModel
from app.infrastructure.repositories._mappers import (
    apply_producto,
    producto_to_entity,
)


class ProductoRepositoryImpl(ProductoRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, producto_id: int) -> Optional[Producto]:
        model = await self._session.get(ProductoModel, producto_id)
        return producto_to_entity(model) if model else None

    async def get_by_codigo(self, codigo: str) -> Optional[Producto]:
        stmt = select(ProductoModel).where(ProductoModel.codigo == codigo)
        model = await self._session.scalar(stmt)
        return producto_to_entity(model) if model else None

    async def list(
        self,
        *,
        skip: int = 0,
        limit: int = 50,
        categoria_id: Optional[int] = None,
        solo_activos: bool = False,
    ) -> list[Producto]:
        stmt = select(ProductoModel)
        if categoria_id is not None:
            stmt = stmt.where(ProductoModel.categoria_id == categoria_id)
        if solo_activos:
            stmt = stmt.where(ProductoModel.activo.is_(True))
        stmt = stmt.order_by(ProductoModel.nombre).offset(skip).limit(limit)
        result = await self._session.scalars(stmt)
        return [producto_to_entity(m) for m in result.all()]

    async def search(self, termino: str, *, limit: int = 20) -> list[Producto]:
        like = f"%{termino.strip()}%"
        stmt = (
            select(ProductoModel)
            .where(
                or_(
                    ProductoModel.nombre.like(like),
                    ProductoModel.codigo.like(like),
                )
            )
            .order_by(ProductoModel.nombre)
            .limit(limit)
        )
        result = await self._session.scalars(stmt)
        return [producto_to_entity(m) for m in result.all()]

    async def count(
        self,
        *,
        categoria_id: Optional[int] = None,
        solo_activos: bool = False,
    ) -> int:
        stmt = select(func.count()).select_from(ProductoModel)
        if categoria_id is not None:
            stmt = stmt.where(ProductoModel.categoria_id == categoria_id)
        if solo_activos:
            stmt = stmt.where(ProductoModel.activo.is_(True))
        return int(await self._session.scalar(stmt) or 0)

    async def create(self, producto: Producto) -> Producto:
        model = ProductoModel()
        apply_producto(producto, model)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return producto_to_entity(model)

    async def update(self, producto: Producto) -> Producto:
        if producto.id is None:
            raise ValueError("El producto debe tener id para actualizarse")
        model = await self._session.get(ProductoModel, producto.id)
        if model is None:
            raise ProductoNoEncontradoError(details={"producto_id": producto.id})
        apply_producto(producto, model)
        await self._session.flush()
        await self._session.refresh(model)
        return producto_to_entity(model)

    async def delete(self, producto_id: int) -> None:
        model = await self._session.get(ProductoModel, producto_id)
        if model is None:
            raise ProductoNoEncontradoError(details={"producto_id": producto_id})
        await self._session.delete(model)
        await self._session.flush()