"""DTOs: Inventario."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class InventarioBaseDTO(BaseModel):
    producto_id: int
    ubicacion_id: int
    cantidad: int = Field(0, ge=0)


class InventarioCreateDTO(InventarioBaseDTO):
    pass


class InventarioUpdateDTO(BaseModel):
    cantidad: int = Field(..., ge=0)


class InventarioReadDTO(InventarioBaseDTO):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fecha_actualizacion: Optional[datetime] = None


class StockPorUbicacionDTO(BaseModel):
    ubicacion_id: int
    codigo_ubicacion: str
    pasillo: str
    estante: str
    nivel: str
    cantidad: int


class StockTotalProductoDTO(BaseModel):
    """Stock consolidado de un producto en todas sus ubicaciones."""

    producto_id: int
    codigo: str
    nombre: str
    unidad_medida: str
    stock_minimo: int
    stock_total: int
    requiere_alerta: bool
    distribucion: list[StockPorUbicacionDTO] = []

class ProductoEnUbicacionResumenDTO(BaseModel):
    """Producto y cantidad dentro de una ubicación."""

    producto_id: int
    codigo: str
    nombre: str
    cantidad: int = Field(0, ge=0)


class UbicacionStockDTO(BaseModel):
    """
    Ubicación con todo lo que hay dentro.

    Es la vista inversa de `StockTotalProductoDTO`: en lugar de "este producto,
    dónde está", responde "esta ubicación, qué tiene". El listado de
    ubicaciones lo necesita y no puede obtenerlo composing las rutas
    existentes, que son de un producto o de una ubicación cada vez.
    """

    ubicacion_id: int
    codigo_ubicacion: str
    pasillo: str
    estante: str
    nivel: str
    productos: list[ProductoEnUbicacionResumenDTO] = []
    total_unidades: int = 0
