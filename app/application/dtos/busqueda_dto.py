"""DTOs: Búsqueda."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.application.dtos.producto_dto import ProductoReadDTO


class IniciarBusquedaDTO(BaseModel):
    termino_busqueda: str = Field(..., min_length=1, max_length=150)
    producto_id: Optional[int] = None


class FinalizarBusquedaDTO(BaseModel):
    ubicacion_encontrada_id: Optional[int] = None
    observaciones: Optional[str] = None


class BusquedaReadDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    usuario_id: int
    producto_id: Optional[int] = None
    producto_nombre: Optional[str] = None
    termino_busqueda: str
    fecha_hora_inicio: Optional[datetime] = None
    fecha_hora_fin: Optional[datetime] = None
    tiempo_busqueda_segundos: Optional[int] = None
    ubicacion_encontrada_id: Optional[int] = None
    exito: bool
    observaciones: Optional[str] = None


class ResultadoBusquedaDTO(BaseModel):
    """
    Resultado que ve el trabajador al buscar un producto:
    el producto + las ubicaciones donde hay stock, ordenadas.
    `busqueda_id` es el id del registro abierto para cerrarlo después.
    """

    busqueda_id: Optional[int] = None
    producto: ProductoReadDTO
    stock_total: int
    ubicaciones: list["UbicacionConStockDTO"]
    

class BusquedaFinalizadaDTO(BusquedaReadDTO):
    """Igual que BusquedaReadDTO, pero semánticamente marca que la búsqueda ya terminó."""
    pass


class UbicacionConStockDTO(BaseModel):
    ubicacion_id: int
    codigo_ubicacion: str
    pasillo: str
    estante: str
    nivel: str
    cantidad: int