"""Endpoints de categorías de productos."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status

from app.application.dtos import (
    CategoriaCreateDTO,
    CategoriaReadDTO,
    CategoriaUpdateDTO,
)
from app.application.use_cases.categorias import (
    CrearCategoriaUseCase,
    ListarCategoriasUseCase,
)
from app.infrastructure.api.dependencies import (
    CategoriaRepoDep,
    SessionDep,
    require_role,
)

router = APIRouter(prefix="/categorias", tags=["categorias"])


# ============================================================
# GET /categorias
# ============================================================
@router.get(
    "/",
    response_model=list[CategoriaReadDTO],
    summary="Listar categorías de productos",
)
async def listar_categorias(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    solo_activas: bool = Query(True),
    categoria_repo: CategoriaRepoDep = None,
) -> list[CategoriaReadDTO]:
    use_case = ListarCategoriasUseCase(categoria_repo)
    return await use_case.execute(skip=skip, limit=limit, solo_activas=solo_activas)


# ============================================================
# POST /categorias
# ============================================================
@router.post(
    "/",
    response_model=CategoriaReadDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva categoría",
    dependencies=[Depends(require_role("Administrador"))],
)
async def crear_categoria(
    payload: CategoriaCreateDTO,
    categoria_repo: CategoriaRepoDep = None,
    session: SessionDep = None,
) -> CategoriaReadDTO:
    use_case = CrearCategoriaUseCase(categoria_repo)
    dto = await use_case.execute(payload)
    # Sin este commit el repositorio solo deja los cambios en la sesión
    # (flush) y se pierden al cerrarla: la API devolvía 201 sin guardar nada.
    await session.commit()
    return dto


# ============================================================
# PATCH /categorias/{id}
# ============================================================
@router.patch(
    "/{categoria_id}",
    response_model=CategoriaReadDTO,
    summary="Actualizar una categoría",
    dependencies=[Depends(require_role("Administrador"))],
)
async def actualizar_categoria(
    categoria_id: int,
    payload: CategoriaUpdateDTO,
    categoria_repo: CategoriaRepoDep = None,
    session: SessionDep = None,
) -> CategoriaReadDTO:
    from app.application.use_cases.categorias import ActualizarCategoriaUseCase
    use_case = ActualizarCategoriaUseCase(categoria_repo)
    dto = await use_case.execute(categoria_id, payload)
    # Ver crear_categoria: sin commit, el PATCH respondía 200 sin cambiar nada.
    await session.commit()
    return dto


# ============================================================
# DELETE /categorias/{id}
# ============================================================
@router.delete(
    "/{categoria_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    summary="Eliminar una categoría",
    dependencies=[Depends(require_role("Administrador"))],
)
async def eliminar_categoria(
    categoria_id: int,
    categoria_repo: CategoriaRepoDep = None,
    session: SessionDep = None,
) -> None:
    from app.application.use_cases.categorias import EliminarCategoriaUseCase
    use_case = EliminarCategoriaUseCase(categoria_repo)
    await use_case.execute(categoria_id)
    # Ver crear_categoria: sin commit, el DELETE respondía 204 sin borrar nada.
    await session.commit()
