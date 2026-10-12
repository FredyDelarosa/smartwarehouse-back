"""
Value Objects del dominio.
Re-exporta todos para imports limpios.
"""

from app.domain.value_objects.codigo_producto import CodigoProducto
from app.domain.value_objects.codigo_ubicacion import CodigoUbicacion
from app.domain.value_objects.email import Email

__all__ = [
    "CodigoProducto",
    "CodigoUbicacion",
    "Email",
]