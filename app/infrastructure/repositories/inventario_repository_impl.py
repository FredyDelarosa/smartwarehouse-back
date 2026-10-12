"""Implementación: InventarioRepository con SQLAlchemy async."""

from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import Inventario, Producto
from app.domain.exceptions import (
    CantidadInvalidaError,
    InventarioNoEncontradoError,
)
from app.domain.repositories import InventarioRepository
from app.infrastructure.database.models import InventarioModel, ProductoModel
from app.infrastructure.repositories._mappers import (
    apply_inventario,
    inventario_to_entity,
    producto_to_entity,
)


class InventarioRepositoryImpl(InventarioRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, inventario_id: int) -> Optional[Inventario]:
        model = await self._session.get(InventarioModel, inventario_id)
        return inventario_to_entity(model) if model else None

    async def get_by_producto_y_ubicacion(
        self, producto_id: int, ubicacion_id: int
    ) -> Optional[Inventario]:
        stmt = select(InventarioModel).where(
            InventarioModel.producto_id == producto_id,
            InventarioModel.ubicacion_id == ubicacion_id,
        )
        model = await self._session.scalar(stmt)
        return inventario_to_entity(model) if model else None

    async def list_by_producto(self, producto_id: int) -> list[Inventario]:
        stmt = select(InventarioModel).where(
            InventarioModel.producto_id == producto_id
        )
        result = await self._session.scalars(stmt)
        return [inventario_to_entity(m) for m in result.all()]

    async def list_by_ubicacion(self, ubicacion_id: int) -> list[Inventario]:
        stmt = select(InventarioModel).where(
            InventarioModel.ubicacion_id == ubicacion_id
        )
        result = await self._session.scalars(stmt)
        return [inventario_to_entity(m) for m in result.all()]

    async def stock_total_producto(self, producto_id: int) -> int:
        stmt = select(func.coalesce(func.sum(InventarioModel.cantidad), 0)).where(
            InventarioModel.producto_id == producto_id
        )
        return int(await self._session.scalar(stmt) or 0)

    async def list_stock_bajo(self) -> list[tuple[Producto, int]]:
        total = func.coalesce(func.sum(InventarioModel.cantidad), 0).label("total")
        stmt = (
            select(ProductoModel, total)
            .join(
                InventarioModel,
                InventarioModel.producto_id == ProductoModel.id,
                isouter=True,
            )
            .group_by(ProductoModel.id)
            .having(total < ProductoModel.stock_minimo)
            .order_by(ProductoModel.nombre)
        )
        result = await self._session.execute(stmt)
        return [(producto_to_entity(pm), int(tot)) for pm, tot in result.all()]

    async def create(self, inventario: Inventario) -> Inventario:
        model = InventarioModel()
        apply_inventario(inventario, model)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return inventario_to_entity(model)

    async def update(self, inventario: Inventario) -> Inventario:
        if inventario.id is None:
            raise ValueError("El inventario debe tener id para actualizarse")
        model = await self._session.get(InventarioModel, inventario.id)
        if model is None:
            raise InventarioNoEncontradoError(
                details={"inventario_id": inventario.id}
            )
        apply_inventario(inventario, model)
        await self._session.flush()
        await self._session.refresh(model)
        return inventario_to_entity(model)

    async def upsert(
        self,
        producto_id: int,
        ubicacion_id: int,
        delta_cantidad: int,
    ) -> Inventario:
        """Crea el registro si no existe, y aplica `delta_cantidad` (puede ser negativo)."""
        stmt = select(InventarioModel).where(
            InventarioModel.producto_id == producto_id,
            InventarioModel.ubicacion_id == ubicacion_id,
        )
        model = await self._session.scalar(stmt)
        if model is None:
            if delta_cantidad < 0:
                raise CantidadInvalidaError(
                    "No se puede decrementar un inventario inexistente",
                    details={
                        "producto_id": producto_id,
                        "ubicacion_id": ubicacion_id,
                        "delta": delta_cantidad,
                    },
                )
            model = InventarioModel(
                producto_id=producto_id,
                ubicacion_id=ubicacion_id,
                cantidad=delta_cantidad,
            )
            self._session.add(model)
        else:
            nueva = model.cantidad + delta_cantidad
            if nueva < 0:
                raise CantidadInvalidaError(
                    "El stock resultante no puede ser negativo",
                    details={
                        "producto_id": producto_id,
                        "ubicacion_id": ubicacion_id,
                        "actual": model.cantidad,
                        "delta": delta_cantidad,
                    },
                )
            model.cantidad = nueva
        await self._session.flush()
        await self._session.refresh(model)
        return inventario_to_entity(model)

    async def delete(self, inventario_id: int) -> None:
        model = await self._session.get(InventarioModel, inventario_id)
        if model is None:
            raise InventarioNoEncontradoError(
                details={"inventario_id": inventario_id}
            )
        await self._session.delete(model)
        await self._session.flush()