"""Caso de uso: obtener un producto por ID."""

from __future__ import annotations

from app.application.dtos import ProductoReadDTO
from app.domain.exceptions import ProductoNoEncontradoError
from app.domain.repositories import ProductoRepository


class ObtenerProductoUseCase:
    def __init__(self, producto_repo: ProductoRepository) -> None:
        self._producto_repo = producto_repo

    async def execute(self, producto_id: int) -> ProductoReadDTO:
        producto = await self._producto_repo.get_by_id(producto_id)
        if producto is None:
            raise ProductoNoEncontradoError(
                details={"producto_id": producto_id}
            )
        return ProductoReadDTO.model_validate(producto)