"""Implementación: CategoriaRepository con SQLAlchemy async."""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities import Categoria
from app.domain.exceptions import EntidadNoEncontradaError
from app.domain.repositories import CategoriaRepository
from app.infrastructure.database.models import CategoriaModel
from app.infrastructure.repositories._mappers import (
    apply_categoria,
    categoria_to_entity,
)


class CategoriaRepositoryImpl(CategoriaRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, categoria_id: int) -> Optional[Categoria]:
        model = await self._session.get(CategoriaModel, categoria_id)
        return categoria_to_entity(model) if model else None

    async def get_by_nombre(self, nombre: str) -> Optional[Categoria]:
        stmt = select(CategoriaModel).where(CategoriaModel.nombre == nombre)
        model = await self._session.scalar(stmt)
        return categoria_to_entity(model) if model else None

    async def list(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        solo_activas: bool = True,
    ) -> list[Categoria]:
        stmt = select(CategoriaModel).order_by(CategoriaModel.id)
        if solo_activas:
            stmt = stmt.where(CategoriaModel.activo.is_(True))
        stmt = stmt.offset(skip).limit(limit)
        result = await self._session.scalars(stmt)
        return [categoria_to_entity(m) for m in result.all()]

    async def create(self, categoria: Categoria) -> Categoria:
        model = CategoriaModel()
        apply_categoria(categoria, model)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return categoria_to_entity(model)

    async def update(self, categoria: Categoria) -> Categoria:
        if categoria.id is None:
            raise ValueError("La categoría debe tener id para actualizarse")
        model = await self._session.get(CategoriaModel, categoria.id)
        if model is None:
            raise EntidadNoEncontradaError(
                "Categoría no encontrada",
                details={"categoria_id": categoria.id},
            )
        apply_categoria(categoria, model)
        await self._session.flush()
        await self._session.refresh(model)
        return categoria_to_entity(model)

    async def delete(self, categoria_id: int) -> None:
        model = await self._session.get(CategoriaModel, categoria_id)
        if model is None:
            raise EntidadNoEncontradaError(
                "Categoría no encontrada", details={"categoria_id": categoria_id}
            )
        await self._session.delete(model)
        await self._session.flush()