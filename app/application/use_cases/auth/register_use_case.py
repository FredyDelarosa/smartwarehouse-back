"""Caso de uso: registrar usuario."""

from __future__ import annotations

from app.application.dtos import UsuarioCreateDTO, UsuarioReadDTO
from app.domain.entities import Usuario
from app.domain.exceptions import (
    DomainError,
    EmailYaRegistradoError,
    EntidadNoEncontradaError,
)
from app.domain.ports import PasswordHasherPort
from app.domain.repositories import RolRepository, UsuarioRepository


class RegisterUseCase:
    def __init__(
        self,
        usuario_repo: UsuarioRepository,
        rol_repo: RolRepository,
        hasher: PasswordHasherPort,
    ) -> None:
        self._usuario_repo = usuario_repo
        self._rol_repo = rol_repo
        self._hasher = hasher

    async def execute(self, dto: UsuarioCreateDTO) -> UsuarioReadDTO:
        email = str(dto.email).lower().strip()

        # 1. Verificar que el email no esté registrado
        if await self._usuario_repo.get_by_email(email) is not None:
            raise EmailYaRegistradoError(details={"email": email})

        # 2. Verificar que el rol exista
        rol = await self._rol_repo.get_by_id(dto.rol_id)
        if rol is None:
            raise EntidadNoEncontradaError(
                "Rol no encontrado", details={"rol_id": dto.rol_id}
            )

        # 3. Hashear password
        password_hash = self._hasher.hash(dto.password)

        # 4. Construir la entidad y persistir
        usuario = Usuario(
            nombre=dto.nombre.strip(),
            email=email,
            password_hash=password_hash,
            rol_id=dto.rol_id,
            activo=dto.activo,
        )
        creado = await self._usuario_repo.create(usuario)

        if creado.id is None:
            raise DomainError("No se pudo obtener el id del usuario creado")

        return UsuarioReadDTO(
            id=creado.id,
            nombre=creado.nombre,
            email=creado.email,
            rol_id=creado.rol_id,
            nombre_rol=rol.nombre,
            activo=creado.activo,
            fecha_creacion=creado.fecha_creacion,
            ultimo_acceso=creado.ultimo_acceso,
        )