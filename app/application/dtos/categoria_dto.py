"""DTOs: Categoría."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CategoriaBaseDTO(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=255)
    activo: bool = True


class CategoriaCreateDTO(CategoriaBaseDTO):
    pass


class CategoriaUpdateDTO(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=255)
    activo: Optional[bool] = None


class CategoriaReadDTO(CategoriaBaseDTO):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: Optional[datetime] = None