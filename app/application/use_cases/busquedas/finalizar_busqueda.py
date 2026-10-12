"""Caso de uso: cerrar una búsqueda y calcular su tiempo."""

from __future__ import annotations

from app.application.dtos import BusquedaFinalizadaDTO, FinalizarBusquedaDTO
from app.domain.exceptions import BusquedaNoEncontradaError
from app.domain.repositories import BusquedaRepository, UbicacionRepository


class FinalizarBusquedaUseCase:
    def __init__(
        self,
        busqueda_repo: BusquedaRepository,
        ubicacion_repo: UbicacionRepository,
    ) -> None:
        self._busqueda_repo = busqueda_repo
        self._ubicacion_repo = ubicacion_repo

    async def execute(
        self, busqueda_id: int, dto: FinalizarBusquedaDTO
    ) -> BusquedaFinalizadaDTO:
        busqueda = await self._busqueda_repo.get_by_id(busqueda_id)
        if busqueda is None:
            raise BusquedaNoEncontradaError(
                details={"busqueda_id": busqueda_id}
            )

        # Si se indica una ubicación, validarla
        if dto.ubicacion_encontrada_id is not None:
            ubicacion = await self._ubicacion_repo.get_by_id(
                dto.ubicacion_encontrada_id
            )
            if ubicacion is None:
                raise BusquedaNoEncontradaError(
                    "Ubicación informada no existe",
                    details={"ubicacion_id": dto.ubicacion_encontrada_id},
                )

        busqueda.finalizar(
            ubicacion_encontrada_id=dto.ubicacion_encontrada_id,
            observaciones=dto.observaciones,
        )
        actualizada = await self._busqueda_repo.update(busqueda)
        return BusquedaFinalizadaDTO.model_validate(actualizada)