"""Caso de uso: crear una incidencia del almacén."""

from __future__ import annotations

from app.application.dtos import IncidenciaCreateDTO, IncidenciaReadDTO
from app.domain.entities import Incidencia
from app.domain.exceptions import (
    ProductoNoEncontradoError,
    UbicacionNoEncontradaError,
)
from app.domain.repositories import (
    IncidenciaRepository,
    ProductoRepository,
    UbicacionRepository,
)


class CrearIncidenciaUseCase:
    def __init__(
        self,
        incidencia_repo: IncidenciaRepository,
        producto_repo: ProductoRepository,
        ubicacion_repo: UbicacionRepository,
    ) -> None:
        self._incidencia_repo = incidencia_repo
        self._producto_repo = producto_repo
        self._ubicacion_repo = ubicacion_repo

    async def execute(
        self, dto: IncidenciaCreateDTO, usuario_id: int
    ) -> IncidenciaReadDTO:
        # 1. Validar producto si se especifica
        if dto.producto_id is not None:
            producto = await self._producto_repo.get_by_id(dto.producto_id)
            if producto is None:
                raise ProductoNoEncontradoError(
                    details={"producto_id": dto.producto_id}
                )

        # 2. Validar ubicación si se especifica
        if dto.ubicacion_id is not None:
            ubicacion = await self._ubicacion_repo.get_by_id(dto.ubicacion_id)
            if ubicacion is None:
                raise UbicacionNoEncontradaError(
                    details={"ubicacion_id": dto.ubicacion_id}
                )

        # 3. Construir y persistir (la fecha la asigna la BD por server_default)
        incidencia = Incidencia(
            tipo=dto.tipo,
            usuario_id=usuario_id,
            producto_id=dto.producto_id,
            ubicacion_id=dto.ubicacion_id,
            descripcion=dto.descripcion,
            resuelta=False,
        )
        creada = await self._incidencia_repo.create(incidencia)
        return IncidenciaReadDTO.model_validate(creada)