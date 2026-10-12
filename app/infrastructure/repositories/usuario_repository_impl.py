"""Implementación: UsuarioRepository con SQLAlchemy async."""

from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.entities import Usuario
from app.domain.exceptions import UsuarioNoEncontradoError
from app.domain.repositories import UsuarioRepository
from app.infrastructure.database.models import UsuarioModel
from app.infrastructure.repositories._mappers import apply_usuario, usuario_to_entity


class UsuarioRepositoryImpl(UsuarioRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, usuario_id: int) -> Optional[Usuario]:
        stmt = (
            select(UsuarioModel)
            .options(selectinload(UsuarioModel.rol))
            .where(UsuarioModel.id == usuario_id)
        )
        model = await self._session.scalar(stmt)
        return usuario_to_entity(model, include_rol=True) if model else None

    async def get_by_email(self, email: str) -> Optional[Usuario]:
        stmt = (
            select(UsuarioModel)
            .options(selectinload(UsuarioModel.rol))
            .where(UsuarioModel.email == email.lower().strip())
        )
        model = await self._session.scalar(stmt)
        return usuario_to_entity(model, include_rol=True) if model else None

    async def list(self, *, solo_activos: bool = False) -> list[Usuario]:
        stmt = select(UsuarioModel).options(selectinload(UsuarioModel.rol))
        if solo_activos:
            stmt = stmt.where(UsuarioModel.activo.is_(True))
        stmt = stmt.order_by(UsuarioModel.id)
        result = await self._session.scalars(stmt)
        return [usuario_to_entity(m, include_rol=True) for m in result.all()]

    async def create(self, usuario: Usuario) -> Usuario:
        model = UsuarioModel()
        apply_usuario(usuario, model)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return usuario_to_entity(model, include_rol=False)

    async def update(self, usuario: Usuario) -> Usuario:
        if usuario.id is None:
            raise ValueError("El usuario debe tener id para actualizarse")
        model = await self._session.get(UsuarioModel, usuario.id)
        if model is None:
            raise UsuarioNoEncontradoError(details={"usuario_id": usuario.id})
        apply_usuario(usuario, model)
        await self._session.flush()
        await self._session.refresh(model)
        return usuario_to_entity(model, include_rol=False)

    async def delete(self, usuario_id: int) -> None:
        model = await self._session.get(UsuarioModel, usuario_id)
        if model is None:
            raise UsuarioNoEncontradoError(details={"usuario_id": usuario_id})
        await self._session.delete(model)
        await self._session.flush()

    async def marcar_acceso(self, usuario_id: int, momento: datetime) -> None:
        model = await self._session.get(UsuarioModel, usuario_id)
        if model is None:
            raise UsuarioNoEncontradoError(details={"usuario_id": usuario_id})
        model.ultimo_acceso = momento
        await self._session.flush()