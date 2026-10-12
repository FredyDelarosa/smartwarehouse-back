"""DTOs: Almacén."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class AlmacenBaseDTO(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    direccion: Optional[str] = Field(None, max_length=255)
    activo: bool = True


class AlmacenCreateDTO(AlmacenBaseDTO):
    pass


class AlmacenUpdateDTO(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    direccion: Optional[str] = Field(None, max_length=255)
    activo: Optional[bool] = None


class AlmacenReadDTO(AlmacenBaseDTO):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: Optional[datetime] = None