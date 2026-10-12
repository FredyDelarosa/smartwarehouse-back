"""DTOs: Movimiento."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.domain.entities import TipoMovimiento


class MovimientoBaseDTO(BaseModel):
    tipo: TipoMovimiento
    producto_id: int
    cantidad: int = Field(..., gt=0)
    ubicacion_origen_id: Optional[int] = None
    ubicacion_destino_id: Optional[int] = None
    referencia: Optional[str] = Field(None, max_length=100)
    observaciones: Optional[str] = None


class MovimientoCreateDTO(MovimientoBaseDTO):
    """Valida que origen/destino sean coherentes con el tipo de movimiento."""

    @model_validator(mode="after")
    def _validar_ubicaciones(self) -> "MovimientoCreateDTO":
        if self.tipo == TipoMovimiento.ENTRADA and self.ubicacion_destino_id is None:
            raise ValueError("Una ENTRADA requiere ubicación destino")
        if self.tipo == TipoMovimiento.SALIDA and self.ubicacion_origen_id is None:
            raise ValueError("Una SALIDA requiere ubicación origen")
        if self.tipo == TipoMovimiento.TRASLADO:
            if self.ubicacion_origen_id is None or self.ubicacion_destino_id is None:
                raise ValueError("Un TRASLADO requiere ubicación origen y destino")
            if self.ubicacion_origen_id == self.ubicacion_destino_id:
                raise ValueError("Origen y destino no pueden ser la misma ubicación")
        if self.tipo == TipoMovimiento.AJUSTE:
            if self.ubicacion_origen_id is None and self.ubicacion_destino_id is None:
                raise ValueError("Un AJUSTE requiere una ubicación afectada")
        return self


class MovimientoReadDTO(MovimientoBaseDTO):
    model_config = ConfigDict(from_attributes=True)

    id: int
    usuario_id: int
    fecha: Optional[datetime] = None