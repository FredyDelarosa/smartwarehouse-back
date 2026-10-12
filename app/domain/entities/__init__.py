"""
Entidades del dominio.
Re-exporta todas las clases para imports limpios.
"""

from app.domain.entities.almacen import Almacen
from app.domain.entities.busqueda import Busqueda
from app.domain.entities.categoria import Categoria
from app.domain.entities.incidencia import Incidencia, TipoIncidencia
from app.domain.entities.inventario import Inventario
from app.domain.entities.movimiento import Movimiento, TipoMovimiento
from app.domain.entities.producto import Producto
from app.domain.entities.rol import Rol
from app.domain.entities.ubicacion import Ubicacion
from app.domain.entities.usuario import Usuario

__all__ = [
    "Almacen",
    "Busqueda",
    "Categoria",
    "Incidencia",
    "TipoIncidencia",
    "Inventario",
    "Movimiento",
    "TipoMovimiento",
    "Producto",
    "Rol",
    "Ubicacion",
    "Usuario",
]