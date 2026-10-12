"""Caso de uso: actualizar una categoría."""

from __future__ import annotations

from app.application.dtos import CategoriaReadDTO, CategoriaUpdateDTO
from app.domain.exceptions import (
    CategoriaNoEncontradaError,
    ValidacionError,
)
from app.domain.exceptions.domain_exceptions import EntidadDuplicadaError
from app.domain.repositories import CategoriaRepository


class ActualizarCategoriaUseCase:
    def __init__(self, categoria_repo: CategoriaRepository) -> None:
        self._categoria_repo = categoria_repo

    async def execute(
        self, categoria_id: int, dto: CategoriaUpdateDTO
    ) -> CategoriaReadDTO:
        categoria = await self._categoria_repo.get_by_id(categoria_id)
        if categoria is None:
            raise CategoriaNoEncontradaError(
                details={"categoria_id": categoria_id}
            )

        # Verificar unicidad del nombre si cambia
        if dto.nombre is not None and dto.nombre != categoria.nombre:
            existente = await self._categoria_repo.get_by_nombre(dto.nombre)
            if existente is not None and existente.id != categoria.id:
                raise EntidadDuplicadaError(
                    "Ya existe una categoría con ese nombre",
                    details={"nombre": dto.nombre},
                )
            categoria.nombre = dto.nombre

        if dto.descripcion is not None:
            categoria.descripcion = dto.descripcion
        if dto.activo is not None:
            categoria.activo = dto.activo

        errores = categoria.validar()
        if errores:
            raise ValidacionError(errores=errores)

        actualizada = await self._categoria_repo.update(categoria)
        return CategoriaReadDTO.model_validate(actualizada)
