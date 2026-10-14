"""Caso de uso: alta de un almacén nuevo con su administrador (PET-4, fase 2)."""

from __future__ import annotations

from app.application.dtos import (
    AlmacenReadDTO,
    OnboardingDTO,
    OnboardingResultDTO,
    TokenDTO,
    UsuarioReadDTO,
)
from app.domain.entities import Almacen, Usuario
from app.domain.exceptions import (
    DomainError,
    EmailYaRegistradoError,
    EntidadNoEncontradaError,
)
from app.domain.ports import PasswordHasherPort, TokenProviderPort
from app.domain.repositories import AlmacenRepository, RolRepository, UsuarioRepository

ROL_ADMINISTRADOR = "Administrador"


class OnboardingUseCase:
    """
    Crea un almacén y su administrador en una sola operación.

    ## Por qué una sola llamada y no dos

    Si el alta fuera "crear almacén" y luego "crear usuario", un fallo entre
    ambas dejaría un almacén huérfano sin dueño, o un usuario apuntando a un
    almacén a medio crear. Aquí las dos cosas van juntas: los repositorios
    hacen `flush()` y la transacción se confirma una vez, en la ruta. O existe
    el almacén con su administrador, o no existe ninguno de los dos.

    ## Por qué Administrador y no el rol que pida el cliente

    Quien da de alta el almacén es su responsable: configura pasillos, genera
    ubicaciones y crea a los demás usuarios. Si se le asignara Supervisor o
    Almacenero, se quedaría sin poder administrar su propio almacén. El rol NO
    se acepta en el cuerpo de la petición a propósito: es una decisión de
    seguridad, no una preferencia del cliente.

    ## El almacén no se ata en el token

    `almacen_id` NO viaja en el JWT. Vive en `usuarios.almacen_id` y lo lee
    `get_current_user` en cada petición. Meterlo en el token obligaría a
    invalidar las sesiones de todos los usuarios cada vez que se moviera a
    alguien de almacén; leerlo de la base hace que el cambio surta efecto
    inmediato, sin dejar tokens viejos dando acceso a un almacén al que ya no
    pertenece.
    """

    def __init__(
        self,
        almacen_repo: AlmacenRepository,
        usuario_repo: UsuarioRepository,
        rol_repo: RolRepository,
        hasher: PasswordHasherPort,
        token_provider: TokenProviderPort,
    ) -> None:
        self._almacen_repo = almacen_repo
        self._usuario_repo = usuario_repo
        self._rol_repo = rol_repo
        self._hasher = hasher
        self._tokens = token_provider

    async def execute(self, dto: OnboardingDTO) -> OnboardingResultDTO:
        email = str(dto.usuario.email).lower().strip()

        # --- Validaciones -------------------------------------------------
        if await self._usuario_repo.get_by_email(email) is not None:
            raise EmailYaRegistradoError(details={"email": email})

        rol_admin = await self._rol_repo.get_by_nombre(ROL_ADMINISTRADOR)
        if rol_admin is None:
            raise EntidadNoEncontradaError(
                "El rol Administrador no existe. Ejecute el seed inicial.",
                details={"rol": ROL_ADMINISTRADOR},
            )

        # --- 1. Almacén ---------------------------------------------------
        almacen = await self._almacen_repo.create(
            Almacen(
                nombre=dto.almacen.nombre.strip(),
                direccion=(dto.almacen.direccion or "").strip() or None,
                activo=True,
            )
        )
        if almacen.id is None:
            raise DomainError("No se pudo crear el almacén.")

        # --- 2. Administrador, atado a ESE almacén ------------------------
        usuario = await self._usuario_repo.create(
            Usuario(
                nombre=dto.usuario.nombre.strip(),
                email=email,
                password_hash=self._hasher.hash(dto.usuario.password),
                rol_id=rol_admin.id,
                almacen_id=almacen.id,
                activo=True,
            )
        )
        if usuario.id is None:
            raise DomainError("No se pudo crear el usuario administrador.")

        # --- 3. Sesión iniciada -------------------------------------------
        # Se devuelve token para que el cliente entre directamente en su
        # almacén: pedirle que escriba la contraseña otra vez nada más de
        # crearla es una fricción absurda en un formulario de dos pasos.
        extra = {"rol": rol_admin.nombre}
        access = self._tokens.create_access_token(subject=usuario.id, extra_claims=extra)
        refresh = self._tokens.create_refresh_token(subject=usuario.id)

        return OnboardingResultDTO(
            almacen=AlmacenReadDTO(
                id=almacen.id,
                nombre=almacen.nombre,
                direccion=almacen.direccion,
                activo=almacen.activo,
                created_at=almacen.created_at,
            ),
            usuario=UsuarioReadDTO(
                id=usuario.id,
                nombre=usuario.nombre,
                email=usuario.email,
                rol_id=rol_admin.id,
                nombre_rol=rol_admin.nombre,
                activo=True,
                fecha_creacion=usuario.fecha_creacion,
            ),
            token=TokenDTO(access_token=access, refresh_token=refresh),
        )