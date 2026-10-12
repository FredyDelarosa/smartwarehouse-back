"""Caso de uso: iniciar sesión."""

from __future__ import annotations

from datetime import datetime, timezone

from app.application.dtos import LoginDTO, TokenDTO
from app.domain.exceptions import (
    CredencialesInvalidasError,
    UsuarioInactivoError,
)
from app.domain.ports import PasswordHasherPort, TokenProviderPort
from app.domain.repositories import UsuarioRepository


class LoginUseCase:
    def __init__(
        self,
        usuario_repo: UsuarioRepository,
        hasher: PasswordHasherPort,
        token_provider: TokenProviderPort,
    ) -> None:
        self._usuario_repo = usuario_repo
        self._hasher = hasher
        self._tokens = token_provider

    async def execute(self, dto: LoginDTO) -> TokenDTO:
        # 1. Buscar usuario por email
        usuario = await self._usuario_repo.get_by_email(str(dto.email))
        if usuario is None or usuario.id is None:
            raise CredencialesInvalidasError()

        # 2. Verificar contraseña
        if not self._hasher.verify(dto.password, usuario.password_hash):
            raise CredencialesInvalidasError()

        # 3. Comprobar que está activo
        if not usuario.puede_autenticarse():
            raise UsuarioInactivoError(details={"usuario_id": usuario.id})

        # 4. Registrar el último acceso
        await self._usuario_repo.marcar_acceso(
            usuario.id, datetime.utcnow()
        )

        # 5. Emitir tokens
        rol_nombre = usuario.nombre_rol
        extra = {"rol": rol_nombre} if rol_nombre else None
        access = self._tokens.create_access_token(
            subject=usuario.id, extra_claims=extra
        )
        refresh = self._tokens.create_refresh_token(subject=usuario.id)

        return TokenDTO(access_token=access, refresh_token=refresh)