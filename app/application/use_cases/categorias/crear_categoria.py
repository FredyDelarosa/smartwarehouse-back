"""Caso de uso: crear una categoría."""

from __future__ import annotations

from app.application.dtos import CategoriaCreateDTO, CategoriaReadDTO
from app.domain.entities import Categoria
from app.domain.exceptions import (
    ValidacionError,
)
from app.domain.exceptions.domain_exceptions import EntidadDuplicadaError
from app.domain.repositories import CategoriaRepository


class CrearCategoriaUseCase:
    def __init__(self, categoria_repo: CategoriaRepository) -> None:
        self._categoria_repo = categoria_repo

    async def execute(self, dto: CategoriaCreateDTO) -> CategoriaReadDTO:
        # Verificar unicidad del nombre
        existente = await self._categoria_repo.get_by_nombre(dto.nombre)
        if existente is not None:
            raise EntidadDuplicadaError(
                "Ya existe una categoría con ese nombre",
                details={"nombre": dto.nombre},
            )

        # Construir y persistir
        categoria = Categoria(
            nombre=dto.nombre,
            descripcion=dto.descripcion,
            activo=dto.activo,
        )
        errores = categoria.validar()
        if errores:
            raise ValidacionError(errores=errores)

        creada = await self._categoria_repo.create(categoria)
        return CategoriaReadDTO.model_validate(creada)
