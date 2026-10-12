"""Caso de uso: crear una ubicación física."""

from __future__ import annotations

from app.application.dtos import UbicacionCreateDTO, UbicacionReadDTO
from app.domain.entities import Ubicacion
from app.domain.exceptions import (
    EntidadNoEncontradaError,
    UbicacionDuplicadaError,
    ValidacionError,
)
from app.domain.repositories import AlmacenRepository, UbicacionRepository
from app.domain.value_objects import CodigoUbicacion


class CrearUbicacionUseCase:
    def __init__(
        self,
        ubicacion_repo: UbicacionRepository,
        almacen_repo: AlmacenRepository,
    ) -> None:
        self._ubicacion_repo = ubicacion_repo
        self._almacen_repo = almacen_repo

    async def execute(self, dto: UbicacionCreateDTO) -> UbicacionReadDTO:
        # 1. Validar y normalizar el código de ubicación con el VO
        try:
            codigo_vo = CodigoUbicacion(dto.codigo_ubicacion)
        except ValueError as exc:
            raise ValidacionError(str(exc), errores=[str(exc)]) from exc

        # 2. Verificar que el almacén exista
        almacen = await self._almacen_repo.get_by_id(dto.almacen_id)
        if almacen is None:
            raise EntidadNoEncontradaError(
                "Almacén no encontrado",
                details={"almacen_id": dto.almacen_id},
            )

        # 3. Verificar unicidad del código
        if await self._ubicacion_repo.get_by_codigo(codigo_vo.valor) is not None:
            raise UbicacionDuplicadaError(
                details={"codigo_ubicacion": codigo_vo.valor}
            )

        # 4. Construir y persistir
        ubicacion = Ubicacion(
            almacen_id=dto.almacen_id,
            pasillo=codigo_vo.pasillo,
            estante=codigo_vo.estante,
            nivel=str(codigo_vo.nivel),
            codigo_ubicacion=codigo_vo.valor,
            codigo_qr=dto.codigo_qr,
            coordenada_x=dto.coordenada_x,
            coordenada_y=dto.coordenada_y,
            activo=dto.activo,
        )
        creada = await self._ubicacion_repo.create(ubicacion)
        return UbicacionReadDTO.model_validate(creada)