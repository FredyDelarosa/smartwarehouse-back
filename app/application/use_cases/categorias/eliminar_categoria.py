"""Caso de uso: eliminar una categoría."""

from __future__ import annotations

from app.domain.exceptions import CategoriaNoEncontradaError
from app.domain.repositories import CategoriaRepository


class EliminarCategoriaUseCase:
    def __init__(self, categoria_repo: CategoriaRepository) -> None:
        self._categoria_repo = categoria_repo

    async def execute(self, categoria_id: int) -> None:
        categoria = await self._categoria_repo.get_by_id(categoria_id)
        if categoria is None:
            raise CategoriaNoEncontradaError(
                details={"categoria_id": categoria_id}
            )
        await self._categoria_repo.delete(categoria_id)
