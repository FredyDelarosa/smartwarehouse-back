"""Endpoints de configuración del almacén (PET-4, fases 3 y 4).

El cuestionario vive en el frontend; estas tres rutas son su respaldo:
previsualizar, generar y consultar el estado.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, status

from app.application.dtos import (
    ConfigAlmacenDTO,
    GeneracionResultDTO,
    PrevisualizacionDTO,
    ResumenAlmacenDTO,
)
from app.application.use_cases.configuracion import ConfigurarAlmacenUseCase
from app.domain.entities import Usuario
from app.infrastructure.api.dependencies import (
    AlmacenRepoDep,
    CurrentUserDep,
    CurrentUserOpcionalDep,
    SessionDep,
    UbicacionRepoDep,
    UbicacionRepoOpcionalDep,
    require_role,
)

router = APIRouter(prefix="/configuracion", tags=["configuracion"])

#: Solo el administrador del almacén define su layout. Un Almacenero que sabe
#: contar estantes no puede decidir la numeración que usarán los demás.
ROLES_ADMIN = ["Administrador"]


def _caso_de_uso(ubicacion_repo) -> ConfigurarAlmacenUseCase:
    return ConfigurarAlmacenUseCase(ubicacion_repo)


# ============================================================
# POST /configuracion/previsualizar   (sin sesión)
# ============================================================
@router.post(
    "/previsualizar",
    response_model=PrevisualizacionDTO,
    summary="Simular la generación sin escribir nada",
)
async def previsualizar(
    payload: ConfigAlmacenDTO,
    current_user: CurrentUserOpcionalDep = None,
    ubicacion_repo: UbicacionRepoOpcionalDep = None,
) -> PrevisualizacionDTO:
    """
    Dice cuántas ubicaciones saldrían y cómo se nombrarían, sin tocar la base.

    Es la pantalla de confirmación: sin ella, el usuario pulsaría "generar" y
    descubriría después que se le habían creado 1.500 estantes.

    ## Por qué NO pide sesión

    El cálculo es puro: sale de las respuestas del cuestionario y no escribe
    nada. Exigir aquí rol de Administrador rompía el flujo de alta, porque
    quien está rellenando el cuestionario todavía no tiene cuenta —la cuenta se
    crea en el último paso—. Le devolvía 401, el interceptor intentaba renovar
    un token que no existía, y el mensaje que veía era "No hay sesión para
    renovar" en lugar de su previsualización.

    Aun así se lee el usuario si viene, y solo para poder contar cuántas de esas
    ubicaciones ya existen en SU almacén y avisar antes de duplicarlas.
    """
    almacen_id = current_user.almacen_id if isinstance(current_user, Usuario) else None
    return await _caso_de_uso(ubicacion_repo).previsualizar(payload, almacen_id)


# ============================================================
# POST /configuracion/generar   (Administrador)
# ============================================================
@router.post(
    "/generar",
    response_model=GeneracionResultDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Crear las ubicaciones descritas en el cuestionario",
    dependencies=[Depends(require_role(*ROLES_ADMIN))],
)
async def generar(
    payload: ConfigAlmacenDTO,
    current_user: CurrentUserDep = None,
    ubicacion_repo: UbicacionRepoDep = None,
    session: SessionDep = None,
) -> GeneracionResultDTO:
    """
    Crea las ubicaciones, sus códigos y sus QR.

    Las que ya existen se omiten en lugar de fallar: repetir la generación es
    normal cuando se añade un pasillo nuevo, y no debería obligar a borrar lo
    que ya funciona para poder continuar.

    Sin este commit las ubicaciones se perderían al cerrar la sesión: el
    endpoint devolvería 201 con un conteo que luego no existiría.
    """
    resultado = await _caso_de_uso(ubicacion_repo).generar(payload, current_user.almacen_id)
    await session.commit()
    return resultado


# ============================================================
# GET /configuracion/almacen
# ============================================================
@router.get(
    "/almacen",
    response_model=ResumenAlmacenDTO,
    summary="Estado actual de las ubicaciones del almacén",
)
async def resumen(
    current_user: CurrentUserDep = None,
    ubicacion_repo: UbicacionRepoDep = None,
    almacen_repo: AlmacenRepoDep = None,
) -> ResumenAlmacenDTO:
    """Sirve para mostrar «tu almacén tiene 96 ubicaciones» o «aún no hay ninguna»."""
    return await ConfigurarAlmacenUseCase(ubicacion_repo, almacen_repo).resumen(
        current_user.almacen_id
    )
