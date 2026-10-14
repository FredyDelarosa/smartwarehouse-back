"""DTOs: Ubicación."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UbicacionBaseDTO(BaseModel):
    """
    `almacen_id` NO se pide al cliente, a propósito.

    Antes era un campo obligatorio del cuerpo y lo rellenaba el formulario con
    un 1 fijo. Eso dejaba la escritura abierta: un administrador de un almacén
    podía crear una ubicación dentro del almacén de otro indicando su id, y el
    receptor la veía en su listado. El almacén lo decide la sesión, no el
    cuerpo de la petición.

    Pydantic ignora los campos extra, así que un cliente antiguo que siga
    mandando `almacen_id` no rompe: el valor se descarta.
    """

    pasillo: str = Field(..., min_length=1, max_length=10)
    estante: str = Field(..., min_length=1, max_length=10)
    nivel: str = Field(..., min_length=1, max_length=10)
    codigo_ubicacion: str = Field(..., min_length=5, max_length=20)
    codigo_qr: Optional[str] = Field(None, max_length=255)
    coordenada_x: Optional[Decimal] = None
    coordenada_y: Optional[Decimal] = None
    activo: bool = True


class UbicacionCreateDTO(UbicacionBaseDTO):
    pass


class UbicacionUpdateDTO(BaseModel):
    pasillo: Optional[str] = Field(None, min_length=1, max_length=10)
    estante: Optional[str] = Field(None, min_length=1, max_length=10)
    nivel: Optional[str] = Field(None, min_length=1, max_length=10)
    codigo_qr: Optional[str] = Field(None, max_length=255)
    coordenada_x: Optional[Decimal] = None
    coordenada_y: Optional[Decimal] = None
    activo: Optional[bool] = None


class UbicacionReadDTO(UbicacionBaseDTO):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: Optional[datetime] = None


class UbicacionQRReadDTO(BaseModel):
    """Respuesta al escanear un QR: la ubicación y los productos que deberían estar ahí."""

    ubicacion: UbicacionReadDTO
    productos: list["ProductoEnUbicacionDTO"]


class ProductoEnUbicacionDTO(BaseModel):
    producto_id: int
    codigo: str
    nombre: str
    cantidad: int