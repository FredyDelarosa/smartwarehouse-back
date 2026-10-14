"""Endpoints de autenticación."""

from __future__ import annotations

from fastapi import APIRouter, Depends, status

from app.application.dtos import (
    ChangePasswordDTO,
    LoginDTO,
    OnboardingDTO,
    OnboardingResultDTO,
    RefreshTokenDTO,
    TokenDTO,
    UsuarioCreateDTO,
    UsuarioReadDTO,
)
from app.application.use_cases.auth import (
    ChangePasswordUseCase,
    LoginUseCase,
    OnboardingUseCase,
    RefreshTokenUseCase,
    RegisterUseCase,
)
from app.infrastructure.api.dependencies import (
    AlmacenRepoDep,
    CurrentUserDep,
    HasherDep,
    RolRepoDep,
    SessionDep,
    TokenProviderDep,
    UsuarioRepoDep,
    require_role,
)

router = APIRouter(prefix="/auth", tags=["auth"])


# ============================================================
# POST /auth/login
# ============================================================
@router.post(
    "/login",
    response_model=TokenDTO,
    summary="Iniciar sesión",
)
async def login(
    payload: LoginDTO,
    usuario_repo: UsuarioRepoDep,
    hasher: HasherDep,
    token_provider: TokenProviderDep,
) -> TokenDTO:
    use_case = LoginUseCase(usuario_repo, hasher, token_provider)
    return await use_case.execute(payload)


# ============================================================
# POST /auth/register  (solo Administrador)
# ============================================================
@router.post(
    "/register",
    response_model=UsuarioReadDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo usuario",
    dependencies=[Depends(require_role("Administrador"))],
)
async def register(
    payload: UsuarioCreateDTO,
    usuario_repo: UsuarioRepoDep,
    rol_repo: RolRepoDep,
    hasher: HasherDep,
    session: SessionDep = None,
) -> UsuarioReadDTO:
    use_case = RegisterUseCase(usuario_repo, rol_repo, hasher)
    dto = await use_case.execute(payload)
    # Sin este commit el usuario se creaba solo en la sesión y se perdía al
    # cerrarla: la API devolvía 201 con un id y luego el login fallaba con 401,
    # como si la cuenta existiera pero la contraseña fuera incorrecta.
    await session.commit()
    return dto


# ============================================================
# POST /auth/refresh
# ============================================================
@router.post(
    "/refresh",
    response_model=TokenDTO,
    summary="Renovar access token usando refresh token",
)
async def refresh(
    payload: RefreshTokenDTO,
    usuario_repo: UsuarioRepoDep,
    token_provider: TokenProviderDep,
) -> TokenDTO:
    use_case = RefreshTokenUseCase(usuario_repo, token_provider)
    return await use_case.execute(payload)


# ============================================================
# POST /auth/change-password
# ============================================================
@router.post(
    "/change-password",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    summary="Cambiar la contraseña del usuario autenticado",
)
async def change_password(
    payload: ChangePasswordDTO,
    current_user: CurrentUserDep,
    usuario_repo: UsuarioRepoDep,
    hasher: HasherDep,
) -> None:
    use_case = ChangePasswordUseCase(usuario_repo, hasher)
    await use_case.execute(current_user.id, payload)


# ============================================================
# GET /auth/me
# ============================================================
@router.get(
    "/me",
    response_model=UsuarioReadDTO,
    summary="Datos del usuario autenticado",
)
async def me(current_user: CurrentUserDep) -> UsuarioReadDTO:
    return UsuarioReadDTO(
        id=current_user.id or 0,
        nombre=current_user.nombre,
        email=current_user.email,
        rol_id=current_user.rol_id,
        nombre_rol=current_user.nombre_rol,
        activo=current_user.activo,
        fecha_creacion=current_user.fecha_creacion,
        ultimo_acceso=current_user.ultimo_acceso,
    )


# ============================================================
# POST /auth/onboarding   (público)
# ============================================================
@router.post(
    "/onboarding",
    response_model=OnboardingResultDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Alta de un almacén nuevo con su administrador",
)
async def onboarding(
    payload: OnboardingDTO,
    almacen_repo: AlmacenRepoDep,
    usuario_repo: UsuarioRepoDep,
    rol_repo: RolRepoDep,
    hasher: HasherDep,
    token_provider: TokenProviderDep,
    session: SessionDep = None,
) -> OnboardingResultDTO:
    """
    Crea el almacén y su administrador y devuelve la sesión ya iniciada.

    Es la ÚNICA ruta pública que escribe en la base. Las demás que crean datos
    exigen rol de Administrador, así que esta es también el punto más expuesto
    del sistema de cara a que alguien se lleve un almacén vacío por spamming.

    Ver la nota de despliegue en DECISIONS.md: para cerrarla del todo hay que
    dejarla detrás de un `rate limit` de nginx o de Cloudflare.
    """
    use_case = OnboardingUseCase(
        almacen_repo, usuario_repo, rol_repo, hasher, token_provider
    )
    dto = await use_case.execute(payload)
    # Un solo commit para el almacén y el usuario: o existen los dos, o ninguno.
    # Si fallara el commit, el token ya emitido apuntaría a un almacén
    # inexistente y el cliente vería un 201 con una sesión muerta.
    await session.commit()
    return dto