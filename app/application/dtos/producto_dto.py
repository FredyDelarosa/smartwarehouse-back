"""DTOs: Producto."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProductoBaseDTO(BaseModel):
    codigo: str = Field(..., min_length=2, max_length=50)
    nombre: str = Field(..., min_length=1, max_length=150)
    descripcion: Optional[str] = None
    categoria_id: Optional[int] = None
    unidad_medida: str = Field("pieza", max_length=20)
    stock_minimo: int = Field(0, ge=0)
    foto_url: Optional[str] = Field(None, max_length=255)
    activo: bool = True


class ProductoCreateDTO(ProductoBaseDTO):
    pass


class ProductoUpdateDTO(BaseModel):
    codigo: Optional[str] = Field(None, min_length=2, max_length=50)
    nombre: Optional[str] = Field(None, min_length=1, max_length=150)
    descripcion: Optional[str] = None
    categoria_id: Optional[int] = None
    unidad_medida: Optional[str] = Field(None, max_length=20)
    stock_minimo: Optional[int] = Field(None, ge=0)
    foto_url: Optional[str] = Field(None, max_length=255)
    activo: Optional[bool] = None


class ProductoReadDTO(ProductoBaseDTO):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None


class ProductoSearchDTO(BaseModel):
    """Parámetros de búsqueda de productos."""

    termino: str = Field(..., min_length=1, max_length=150)
    limit: int = Field(20, ge=1, le=100)