"""Caso de uso: marcar una incidencia como resuelta."""

from __future__ import annotations

from app.application.dtos import IncidenciaReadDTO
from app.domain.exceptions import IncidenciaNoEncontradaError, ValidacionError
from app.domain.repositories import IncidenciaRepository


class ResolverIncidenciaUseCase:
    def __init__(self, incidencia_repo: IncidenciaRepository) -> None:
        self._incidencia_repo = incidencia_repo

    async def execute(self, incidencia_id: int) -> IncidenciaReadDTO:
        incidencia = await self._incidencia_repo.get_by_id(incidencia_id)
        if incidencia is None:
            raise IncidenciaNoEncontradaError(
                details={"incidencia_id": incidencia_id}
            )

        if incidencia.resuelta:
            raise ValidacionError(
                "La incidencia ya estaba resuelta",
                errores=[f"incidencia {incidencia_id} ya resuelta"],
            )

        incidencia.resolver()
        actualizada = await self._incidencia_repo.update(incidencia)
        return IncidenciaReadDTO.model_validate(actualizada)