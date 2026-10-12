"""DTOs: Incidencia."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.domain.entities import TipoIncidencia


class IncidenciaCreateDTO(BaseModel):
    tipo: TipoIncidencia
    producto_id: Optional[int] = None
    ubicacion_id: Optional[int] = None
    descripcion: Optional[str] = None


class IncidenciaUpdateDTO(BaseModel):
    tipo: Optional[TipoIncidencia] = None
    descripcion: Optional[str] = None
    resuelta: Optional[bool] = None


class IncidenciaReadDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tipo: TipoIncidencia
    producto_id: Optional[int] = None
    ubicacion_id: Optional[int] = None
    usuario_id: int
    fecha: Optional[datetime] = None
    descripcion: Optional[str] = None
    resuelta: bool
    fecha_resolucion: Optional[datetime] = None