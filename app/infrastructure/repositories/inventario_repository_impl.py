"""Implementación: InventarioRepository con SQLAlchemy async."""

from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import Inventario, Producto, Ubicacion
from app.domain.exceptions import (
    CantidadInvalidaError,
    InventarioNoEncontradoError,
)
from app.domain.repositories import InventarioRepository
from app.infrastructure.database.models import (
    InventarioModel,
    ProductoModel,
    UbicacionModel,
)
from app.infrastructure.repositories._mappers import (
    apply_inventario,
    inventario_to_entity,
    producto_to_entity,
    ubicacion_to_entity,
)


class InventarioRepositoryImpl(InventarioRepository):
    def __init__(self, session: AsyncSession, *, almacen_id: int | None = None) -> None:
        self._session = session
        # Multialmacén: el stock pertenece a un almacén. Una fila de inventario
        # cuelga de un producto, y el producto ya pertenece a un almacén, así
        # que basta con filtrar por `productos.almacen_id`: no hace falta
        # desnormalizar la tabla `inventario`.
        self._almacen_id = almacen_id

    def _acotar(self, stmt):
        """
        Añade el filtro de almacén a una consulta sobre inventario.

        Se centraliza para que ninguna lectura se quede sin acotar por olvido:
        una consulta sin filtro devolvería el stock de otro almacén sin fallar
        nada, que es el fallo más difícil de detectar.
        """
        if self._almacen_id is None:
            return stmt
        return stmt.join(
            ProductoModel, ProductoModel.id == InventarioModel.producto_id
        ).where(ProductoModel.almacen_id == self._almacen_id)

    async def get_by_id(self, inventario_id: int) -> Optional[Inventario]:
        stmt = self._acotar(select(InventarioModel)).where(
            InventarioModel.id == inventario_id
        )
        model = await self._session.scalar(stmt)
        return inventario_to_entity(model) if model else None

    async def get_by_producto_y_ubicacion(
        self, producto_id: int, ubicacion_id: int
    ) -> Optional[Inventario]:
        stmt = self._acotar(select(InventarioModel)).where(
            InventarioModel.producto_id == producto_id,
            InventarioModel.ubicacion_id == ubicacion_id,
        )
        model = await self._session.scalar(stmt)
        return inventario_to_entity(model) if model else None

    async def list_by_producto(self, producto_id: int) -> list[Inventario]:
        stmt = self._acotar(select(InventarioModel)).where(
            InventarioModel.producto_id == producto_id
        )
        result = await self._session.scalars(stmt)
        return [inventario_to_entity(m) for m in result.all()]

    async def list_by_ubicacion(self, ubicacion_id: int) -> list[Inventario]:
        stmt = self._acotar(select(InventarioModel)).where(
            InventarioModel.ubicacion_id == ubicacion_id
        )
        result = await self._session.scalars(stmt)
        return [inventario_to_entity(m) for m in result.all()]

    async def stock_total_producto(self, producto_id: int) -> int:
        stmt = self._acotar(
            select(func.coalesce(func.sum(InventarioModel.cantidad), 0))
        ).where(InventarioModel.producto_id == producto_id)
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
        # El filtro va directo y no por `_acotar()`: aquí la consulta ya parte
        # de ProductoModel, y volver a hacer join generaría un JOIN duplicado.
        if self._almacen_id is not None:
            stmt = stmt.where(ProductoModel.almacen_id == self._almacen_id)
        result = await self._session.execute(stmt)
        return [(producto_to_entity(pm), int(tot)) for pm, tot in result.all()]

    async def listar_con_productos(
        self,
        *,
        skip: int = 0,
        limit: int = 50,
        solo_activas: bool = True,
    ) -> list[tuple[Ubicacion, list[tuple[Producto, int]]]]:
        """
        JOIN de inventario + ubicaciones + productos.

        La paginación va sobre **ubicaciones**, no sobre las filas del join: con
        un estante que tuviera diez productos, paginar por fila lo repetiría
        diez veces y dejaría huecos en el catálogo. Se resuelve con una
        subconsulta que primero recorta el ids de ubicación.

        La subconsulta ordena también por `codigo_ubicacion`, igual que el SELECT
        exterior. Paginar por `id` y presentar por código daría páginas
        incoherentes: el usuario vería P1-A-01 después de P3-D-02.

        El filtro de almacén va en **las dos** consultas. Es tentador ponerlo solo
        en la exterior, donde se lee el producto, y olvidarlo en la subconsulta
        de ids: entonces `in_(paginadas)` traía filas de otros almacenes y se
        colaban. Pasó: el almacén 1 veía la ubicación P1-A-01 del almacén 2, con
        su producto y su cantidad.
        """
        paginadas = (
            select(InventarioModel.ubicacion_id)
            .join(UbicacionModel, UbicacionModel.id == InventarioModel.ubicacion_id)
            .group_by(InventarioModel.ubicacion_id, UbicacionModel.codigo_ubicacion)
            .order_by(UbicacionModel.codigo_ubicacion)
            .limit(limit)
            .offset(skip)
        )
        if self._almacen_id is not None:
            paginadas = paginadas.where(UbicacionModel.almacen_id == self._almacen_id)

        stmt = (
            select(UbicacionModel, ProductoModel, InventarioModel.cantidad)
            .join(UbicacionModel, UbicacionModel.id == InventarioModel.ubicacion_id)
            .join(ProductoModel, ProductoModel.id == InventarioModel.producto_id)
            .where(InventarioModel.ubicacion_id.in_(paginadas))
            .order_by(UbicacionModel.codigo_ubicacion, ProductoModel.codigo)
        )
        if self._almacen_id is not None:
            stmt = stmt.where(UbicacionModel.almacen_id == self._almacen_id)
        if solo_activas:
            stmt = stmt.where(UbicacionModel.activo.is_(True))

        result = await self._session.execute(stmt)

        agrupado: dict[int, tuple[Ubicacion, list[tuple[Producto, int]]]] = {}
        for um, pm, cantidad in result.all():
            entrada = agrupado.get(um.id)
            if entrada is None:
                ubicacion = ubicacion_to_entity(um)
                entrada = (ubicacion, [])
                agrupado[um.id] = entrada
            entrada[1].append((producto_to_entity(pm), int(cantidad)))

        # El orden del SELECT ya viene por codigo_ubicacion, pero un dict
        # conserva el de inserción en CPython: no hay que reordenar.
        return list(agrupado.values())

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
        stmt = self._acotar(select(InventarioModel)).where(
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