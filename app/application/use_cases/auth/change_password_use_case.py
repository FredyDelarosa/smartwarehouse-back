"""Caso de uso: cambiar contraseña de un usuario autenticado."""

from __future__ import annotations

from app.application.dtos import ChangePasswordDTO
from app.domain.exceptions import (
    CredencialesInvalidasError,
    UsuarioNoEncontradoError,
)
from app.domain.ports import PasswordHasherPort
from app.domain.repositories import UsuarioRepository


class ChangePasswordUseCase:
    def __init__(
        self,
        usuario_repo: UsuarioRepository,
        hasher: PasswordHasherPort,
    ) -> None:
        self._usuario_repo = usuario_repo
        self._hasher = hasher

    async def execute(self, usuario_id: int, dto: ChangePasswordDTO) -> None:
        usuario = await self._usuario_repo.get_by_id(usuario_id)
        if usuario is None:
            raise UsuarioNoEncontradoError(details={"usuario_id": usuario_id})

        if not self._hasher.verify(dto.password_actual, usuario.password_hash):
            raise CredencialesInvalidasError(
                "La contraseña actual no es correcta"
            )

        usuario.password_hash = self._hasher.hash(dto.password_nuevo)
        await self._usuario_repo.update(usuario)