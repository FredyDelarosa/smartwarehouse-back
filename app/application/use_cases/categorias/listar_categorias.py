"""Caso de uso: listar categorías."""

from __future__ import annotations

from app.application.dtos import CategoriaReadDTO
from app.domain.repositories import CategoriaRepository


class ListarCategoriasUseCase:
    def __init__(self, categoria_repo: CategoriaRepository) -> None:
        self._categoria_repo = categoria_repo

    async def execute(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        solo_activas: bool = True,
    ) -> list[CategoriaReadDTO]:
        categorias = await self._categoria_repo.list(
            skip=skip, limit=limit, solo_activas=solo_activas
        )
        return [CategoriaReadDTO.model_validate(c) for c in categorias]
