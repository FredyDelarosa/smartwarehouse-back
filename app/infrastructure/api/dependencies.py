"""
Dependencias de FastAPI (composition root).

Aquí se ensamblan repositorios, puertos y casos de uso. Los endpoints
se limitan a inyectar y ejecutar.
"""

from __future__ import annotations

from typing import Annotated, AsyncIterator

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.domain.entities import Usuario
from app.domain.ports import PasswordHasherPort, TokenProviderPort
from app.domain.repositories import (
    AlmacenRepository,
    BusquedaRepository,
    CategoriaRepository,
    IncidenciaRepository,
    InventarioRepository,
    MovimientoRepository,
    ProductoRepository,
    RolRepository,
    UbicacionRepository,
    UsuarioRepository,
)
from app.infrastructure.database.session import get_session
from app.infrastructure.repositories import (
    AlmacenRepositoryImpl,
    BusquedaRepositoryImpl,
    CategoriaRepositoryImpl,
    IncidenciaRepositoryImpl,
    InventarioRepositoryImpl,
    MovimientoRepositoryImpl,
    ProductoRepositoryImpl,
    RolRepositoryImpl,
    UbicacionRepositoryImpl,
    UsuarioRepositoryImpl,
)
from app.infrastructure.security import BcryptPasswordHasher, JWTTokenProvider


# ============================================================
# Sesión de BD
# ============================================================
SessionDep = Annotated[AsyncSession, Depends(get_session)]


# ============================================================
# Puertos de seguridad (singletons stateless)
# ============================================================
_password_hasher = BcryptPasswordHasher()
_token_provider = JWTTokenProvider()


def get_password_hasher() -> PasswordHasherPort:
    return _password_hasher


def get_token_provider() -> TokenProviderPort:
    return _token_provider


HasherDep = Annotated[PasswordHasherPort, Depends(get_password_hasher)]
TokenProviderDep = Annotated[TokenProviderPort, Depends(get_token_provider)]


# ============================================================
# Repositorios (uno por request, ligado a la sesión)
# ============================================================
# PET-4 · Multialmacén
#
# Los repositorios de datos están ATADOS al almacén del usuario autenticado en
# el momento de construirse, en vez de recibir `almacen_id` en cada método.
#
# Por qué así y no como parámetro: con el parámetro, olvidar el filtro en una
# consulta nueva devuelve datos de otro almacén sin que nada falle. Atándolo en
# el constructor, el olvido no es representable. Además evita cambiar la firma
# de ~40 métodos y todas sus llamadas.
#
# `almacen_id` es obligatorio en el constructor justamente para que no se pueda
# construir un repositorio "desacoplado" por accidente.
#
# Excepción: el repositorio de usuarios NO se ata. Es la fuente de la identidad
# —`get_current_user` lo necesita para saber qué almacén es— y atarlo
# produciría una dependencia circular.

# Tipo auxiliar para los repositorios atados al almacén.
AlmacenScope = int


def get_rol_repo(session: SessionDep) -> RolRepository:
    return RolRepositoryImpl(session)


def get_usuario_repo(session: SessionDep) -> UsuarioRepository:
    return UsuarioRepositoryImpl(session)


def get_almacen_repo(session: SessionDep) -> AlmacenRepository:
    return AlmacenRepositoryImpl(session)


def get_categoria_repo(session: SessionDep) -> CategoriaRepository:
    return CategoriaRepositoryImpl(session)


def get_producto_repo(session: SessionDep, usuario: CurrentUserDep) -> ProductoRepository:
    return ProductoRepositoryImpl(session, almacen_id=usuario.almacen_id)


def get_ubicacion_repo(session: SessionDep, usuario: CurrentUserDep) -> UbicacionRepository:
    return UbicacionRepositoryImpl(session, almacen_id=usuario.almacen_id)


def get_inventario_repo(session: SessionDep, usuario: CurrentUserDep) -> InventarioRepository:
    return InventarioRepositoryImpl(session, almacen_id=usuario.almacen_id)


def get_movimiento_repo(session: SessionDep, usuario: CurrentUserDep) -> MovimientoRepository:
    return MovimientoRepositoryImpl(session, almacen_id=usuario.almacen_id)


def get_busqueda_repo(session: SessionDep, usuario: CurrentUserDep) -> BusquedaRepository:
    return BusquedaRepositoryImpl(session, almacen_id=usuario.almacen_id)


def get_incidencia_repo(session: SessionDep, usuario: CurrentUserDep) -> IncidenciaRepository:
    return IncidenciaRepositoryImpl(session, almacen_id=usuario.almacen_id)


RolRepoDep = Annotated[RolRepository, Depends(get_rol_repo)]
UsuarioRepoDep = Annotated[UsuarioRepository, Depends(get_usuario_repo)]
AlmacenRepoDep = Annotated[AlmacenRepository, Depends(get_almacen_repo)]
CategoriaRepoDep = Annotated[CategoriaRepository, Depends(get_categoria_repo)]
ProductoRepoDep = Annotated[ProductoRepository, Depends(get_producto_repo)]
UbicacionRepoDep = Annotated[UbicacionRepository, Depends(get_ubicacion_repo)]
InventarioRepoDep = Annotated[InventarioRepository, Depends(get_inventario_repo)]
MovimientoRepoDep = Annotated[MovimientoRepository, Depends(get_movimiento_repo)]
BusquedaRepoDep = Annotated[BusquedaRepository, Depends(get_busqueda_repo)]
IncidenciaRepoDep = Annotated[IncidenciaRepository, Depends(get_incidencia_repo)]


# ============================================================
# Autenticación y autorización
# ============================================================
bearer_scheme = HTTPBearer(auto_error=False)


async def get_bearer_token(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None, Depends(bearer_scheme)
    ],
) -> str:
    if credentials is None or not credentials.credentials:
        raise UnauthorizedError("Token de autenticación no proporcionado")
    return credentials.credentials


async def get_current_user(
    token: Annotated[str, Depends(get_bearer_token)],
    token_provider: TokenProviderDep,
    usuario_repo: UsuarioRepoDep,
) -> Usuario:
    try:
        payload = token_provider.decode(token)
    except JWTError as exc:
        raise UnauthorizedError("Token inválido o expirado") from exc

    if payload.get("type") != "access":
        raise UnauthorizedError("El token no es de tipo access")

    sub = payload.get("sub")
    if sub is None:
        raise UnauthorizedError("Token sin sujeto")

    try:
        usuario_id = int(sub)
    except (TypeError, ValueError) as exc:
        raise UnauthorizedError("Sujeto inválido en el token") from exc

    usuario = await usuario_repo.get_by_id(usuario_id)
    if usuario is None:
        raise UnauthorizedError("Usuario no existe")

    if not usuario.puede_autenticarse():
        raise ForbiddenError("El usuario está inactivo")

    return usuario


CurrentUserDep = Annotated[Usuario, Depends(get_current_user)]


def require_role(*roles: str):
    """
    Dependencia parametrizada para RBAC.

    Uso:
        @router.post("/", dependencies=[Depends(require_role("Administrador"))])
        async def crear(...): ...
    """

    async def checker(current_user: CurrentUserDep) -> Usuario:
        rol_nombre = current_user.nombre_rol
        if rol_nombre is None or rol_nombre not in roles:
            raise ForbiddenError(
                f"Se requiere uno de los roles: {', '.join(roles)}"
            )
        return current_user

    return checker