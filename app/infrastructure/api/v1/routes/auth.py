"""Endpoints de autenticación."""

from __future__ import annotations

from fastapi import APIRouter, Depends, status

from app.application.dtos import (
    ChangePasswordDTO,
    LoginDTO,
    RefreshTokenDTO,
    TokenDTO,
    UsuarioCreateDTO,
    UsuarioReadDTO,
)
from app.application.use_cases.auth import (
    ChangePasswordUseCase,
    LoginUseCase,
    RefreshTokenUseCase,
    RegisterUseCase,
)
from app.infrastructure.api.dependencies import (
    CurrentUserDep,
    HasherDep,
    RolRepoDep,
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
) -> UsuarioReadDTO:
    use_case = RegisterUseCase(usuario_repo, rol_repo, hasher)
    return await use_case.execute(payload)


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