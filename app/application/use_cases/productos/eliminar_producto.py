"""Caso de uso: dar de baja un producto (baja lógica)."""

from __future__ import annotations

from app.domain.exceptions import ProductoNoEncontradoError
from app.domain.repositories import ProductoRepository


class EliminarProductoUseCase:
    """
    Baja lógica: marca `activo=False` en lugar de borrar la fila.
    Motivo: preservar integridad referencial con inventario, movimientos,
    búsquedas e incidencias.
    """

    def __init__(self, producto_repo: ProductoRepository) -> None:
        self._producto_repo = producto_repo

    async def execute(self, producto_id: int) -> None:
        producto = await self._producto_repo.get_by_id(producto_id)
        if producto is None:
            raise ProductoNoEncontradoError(
                details={"producto_id": producto_id}
            )
        producto.activo = False
        await self._producto_repo.update(producto)