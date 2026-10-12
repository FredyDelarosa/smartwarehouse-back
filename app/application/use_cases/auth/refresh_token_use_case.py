"""Caso de uso: renovar access token a partir de un refresh token."""

from __future__ import annotations

from jose import JWTError

from app.application.dtos import RefreshTokenDTO, TokenDTO
from app.domain.exceptions import CredencialesInvalidasError
from app.domain.ports import TokenProviderPort
from app.domain.repositories import UsuarioRepository


class RefreshTokenUseCase:
    def __init__(
        self,
        usuario_repo: UsuarioRepository,
        token_provider: TokenProviderPort,
    ) -> None:
        self._usuario_repo = usuario_repo
        self._tokens = token_provider

    async def execute(self, dto: RefreshTokenDTO) -> TokenDTO:
        try:
            payload = self._tokens.decode(dto.refresh_token)
        except JWTError as exc:
            raise CredencialesInvalidasError("Refresh token inválido") from exc

        if payload.get("type") != "refresh":
            raise CredencialesInvalidasError("El token no es de tipo refresh")

        sub = payload.get("sub")
        if sub is None:
            raise CredencialesInvalidasError("Refresh token sin sujeto")

        try:
            usuario_id = int(sub)
        except (TypeError, ValueError) as exc:
            raise CredencialesInvalidasError("Sujeto inválido en el token") from exc

        usuario = await self._usuario_repo.get_by_id(usuario_id)
        if usuario is None or not usuario.puede_autenticarse():
            raise CredencialesInvalidasError("Usuario no válido para renovar")

        rol_nombre = usuario.nombre_rol
        extra = {"rol": rol_nombre} if rol_nombre else None
        access = self._tokens.create_access_token(
            subject=usuario.id, extra_claims=extra
        )
        refresh = self._tokens.create_refresh_token(subject=usuario.id)

        return TokenDTO(access_token=access, refresh_token=refresh)