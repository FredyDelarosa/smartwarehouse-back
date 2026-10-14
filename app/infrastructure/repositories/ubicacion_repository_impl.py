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
    def __init__(self, session: AsyncSession, *, almacen_id: int | None = None) -> None:
        self._session = session
        # `None` solo para el seeding y los scripts de arranque, que necesitan
        # operar sobre todos los almacenes. Las peticiones HTTP siempre lo
        # pasan atado al usuario (ver get_ubicacion_repo).
        self._almacen_id = almacen_id

    async def get_by_id(self, ubicacion_id: int) -> Optional[Ubicacion]:
        stmt = select(UbicacionModel).where(UbicacionModel.id == ubicacion_id)
        if self._almacen_id is not None:
            stmt = stmt.where(UbicacionModel.almacen_id == self._almacen_id)
        model = await self._session.scalar(stmt)
        return ubicacion_to_entity(model) if model else None

    async def get_by_codigo(self, codigo: str) -> Optional[Ubicacion]:
        stmt = select(UbicacionModel).where(
            UbicacionModel.codigo_ubicacion == codigo.strip().upper()
        )
        # El filtro de almacén NO es opcional aquí. El código es único POR
        # ALMACÉN, no en toda la tabla: P1-A-01 existe legítimamente en
        # cualquier número de almacenes. Sin acotar, la búsqueda se llevaba el
        # código del primero que encuentre en la base, y al generar las
        # ubicaciones de un almacén nuevo se respondería que ya existían
        # todas: ninguna.
        if self._almacen_id is not None:
            stmt = stmt.where(UbicacionModel.almacen_id == self._almacen_id)
        model = await self._session.scalar(stmt)
        return ubicacion_to_entity(model) if model else None

    async def get_by_qr(self, codigo_qr: str) -> Optional[Ubicacion]:
        stmt = select(UbicacionModel).where(UbicacionModel.codigo_qr == codigo_qr)
        if self._almacen_id is not None:
            stmt = stmt.where(UbicacionModel.almacen_id == self._almacen_id)
        model = await self._session.scalar(stmt)
        return ubicacion_to_entity(model) if model else None

    # Va ANTES que `list` a propósito: desde ahí en adelante, `list` es el
    # método de esta clase y las anotaciones `list[Ubicacion]` de abajo
    # romperían con "'function' object is not subscriptable".
    async def create_many(
        self, ubicaciones: list[Ubicacion], *, almacen_id: int
    ) -> list[Ubicacion]:
        if not ubicaciones:
            return []

        # Comprobación de ámbito. `create()` no la tiene porque usa el
        # `almacen_id` que trae la entidad; aquí el id viene del parámetro y
        # podría ser de otro almacén si alguien lo manipulase.
        if self._almacen_id is not None and almacen_id != self._almacen_id:
            raise ValueError(
                "No se pueden crear ubicaciones en un almacén distinto "
                "al del usuario autenticado."
            )

        modelos = []
        for ubicacion in ubicaciones:
            m = UbicacionModel()
            apply_ubicacion(ubicacion, m)
            # La entidad no lleva almacén: se lo pone el repositorio, para que
            # el código que genera nunca pueda equivocarse de alcance.
            m.almacen_id = almacen_id
            modelos.append(m)

        self._session.add_all(modelos)
        # Un solo flush para todas. Con flush por fila serían cientos de
        # viajes al servidor solo por el INSERT.
        await self._session.flush()
        for m in modelos:
            await self._session.refresh(m)
        return [ubicacion_to_entity(m) for m in modelos]

    async def list_by_almacen(
        self, almacen_id: int, *, solo_activas: bool = True
    ) -> list[Ubicacion]:
        stmt = select(UbicacionModel).where(UbicacionModel.almacen_id == almacen_id)
        if self._almacen_id is not None:
            # Sin esto, GET /ubicaciones/almacen/{id} aceptaría en la URL el id
            # de OTRO almacén y devolvería sus estantes. El repositorio ya está
            # acotado, pero el id de la ruta viene de fuera y hay que
            # comprobar que coincide con el ámbito del usuario.
            stmt = stmt.where(UbicacionModel.almacen_id == self._almacen_id)
        if solo_activas:
            stmt = stmt.where(UbicacionModel.activo.is_(True))
        stmt = stmt.order_by(
            UbicacionModel.pasillo, UbicacionModel.estante, UbicacionModel.nivel
        )
        result = await self._session.scalars(stmt)
        return [ubicacion_to_entity(m) for m in result.all()]

    async def list(self, *, skip: int = 0, limit: int = 100) -> list[Ubicacion]:
        stmt = select(UbicacionModel)
        if self._almacen_id is not None:
            stmt = stmt.where(UbicacionModel.almacen_id == self._almacen_id)
        stmt = (
            stmt.order_by(
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
        stmt = select(UbicacionModel).where(UbicacionModel.id == ubicacion.id)
        if self._almacen_id is not None:
            stmt = stmt.where(UbicacionModel.almacen_id == self._almacen_id)
        model = await self._session.scalar(stmt)
        if model is None:
            raise UbicacionNoEncontradaError(
                details={"ubicacion_id": ubicacion.id}
            )
        apply_ubicacion(ubicacion, model)
        await self._session.flush()
        await self._session.refresh(model)
        return ubicacion_to_entity(model)

    async def delete(self, ubicacion_id: int) -> None:
        stmt = select(UbicacionModel).where(UbicacionModel.id == ubicacion_id)
        if self._almacen_id is not None:
            stmt = stmt.where(UbicacionModel.almacen_id == self._almacen_id)
        model = await self._session.scalar(stmt)
        if model is None:
            raise UbicacionNoEncontradaError(details={"ubicacion_id": ubicacion_id})
        await self._session.delete(model)
        await self._session.flush()