"""Caso de uso: listar productos con paginación."""

from __future__ import annotations

from typing import Optional

from app.application.dtos import ProductoReadDTO
from app.domain.repositories import ProductoRepository


class ListarProductosUseCase:
    def __init__(self, producto_repo: ProductoRepository) -> None:
        self._producto_repo = producto_repo

    async def execute(
        self,
        *,
        skip: int = 0,
        limit: int = 50,
        categoria_id: Optional[int] = None,
        solo_activos: bool = False,
    ) -> tuple[list[ProductoReadDTO], int]:
        productos = await self._producto_repo.list(
            skip=skip,
            limit=limit,
            categoria_id=categoria_id,
            solo_activos=solo_activos,
        )
        total = await self._producto_repo.count(
            categoria_id=categoria_id, solo_activos=solo_activos
        )
        return [ProductoReadDTO.model_validate(p) for p in productos], total