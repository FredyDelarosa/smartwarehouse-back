"""DTOs: alta de almacén con su administrador (PET-4, fase 2)."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.application.dtos.almacen_dto import AlmacenReadDTO
from app.application.dtos.auth_dto import TokenDTO
from app.application.dtos.usuario_dto import UsuarioReadDTO


class OnboardingAlmacenDTO(BaseModel):
    """Datos mínimos del almacén. Lo demás lo define el cuestionario (fase 3)."""

    nombre: str = Field(..., min_length=1, max_length=100)
    direccion: Optional[str] = Field(None, max_length=255)


class OnboardingUsuarioDTO(BaseModel):
    """
    Datos del responsable del almacén.

    La contraseña se recibe en plano solo aquí; el caso de uso la hashea antes de
    construir la entidad. El campo `rol_id` NO existe a propósito: quien da de
    alta el almacén es su administrador, y admitir el rol desde el cuerpo sería
    permitir que alguien se autoasignara permisos.
    """

    nombre: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)


class OnboardingDTO(BaseModel):
    almacen: OnboardingAlmacenDTO
    usuario: OnboardingUsuarioDTO


class OnboardingResultDTO(BaseModel):
    """
    Alta completada.

    Se devuelven el almacén, el usuario y el token porque el cliente debe
    quedar dentro de su espacio sin que tenga que escribir la contraseña otra
    vez: acaba de crearla en el paso anterior del formulario.
    """

    almacen: AlmacenReadDTO
    usuario: UsuarioReadDTO
    token: TokenDTO