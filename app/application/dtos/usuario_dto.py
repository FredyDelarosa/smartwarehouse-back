"""DTOs: Usuario."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UsuarioBaseDTO(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    rol_id: int
    activo: bool = True


class UsuarioCreateDTO(UsuarioBaseDTO):
    """
    El password se recibe en plano SOLO aquí.
    El caso de uso lo hashea antes de construir la entidad.
    """

    password: str = Field(..., min_length=8, max_length=72)


class UsuarioUpdateDTO(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    rol_id: Optional[int] = None
    activo: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8, max_length=72)


class UsuarioReadDTO(BaseModel):
    """
    El password NUNCA se expone.
    El rol se aplana a nombre_rol para no anidar objetos.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    email: EmailStr
    rol_id: int
    nombre_rol: Optional[str] = None
    activo: bool
    fecha_creacion: Optional[datetime] = None
    ultimo_acceso: Optional[datetime] = None