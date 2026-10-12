"""
Puertos del dominio (interfaces abstractas de repositorios).
Se implementan en `app.infrastructure.repositories`.
"""

from app.domain.repositories.almacen_repository import AlmacenRepository
from app.domain.repositories.busqueda_repository import BusquedaRepository
from app.domain.repositories.categoria_repository import CategoriaRepository
from app.domain.repositories.incidencia_repository import IncidenciaRepository
from app.domain.repositories.inventario_repository import InventarioRepository
from app.domain.repositories.movimiento_repository import MovimientoRepository
from app.domain.repositories.producto_repository import ProductoRepository
from app.domain.repositories.rol_repository import RolRepository
from app.domain.repositories.ubicacion_repository import UbicacionRepository
from app.domain.repositories.usuario_repository import UsuarioRepository

__all__ = [
    "AlmacenRepository",
    "BusquedaRepository",
    "CategoriaRepository",
    "IncidenciaRepository",
    "InventarioRepository",
    "MovimientoRepository",
    "ProductoRepository",
    "RolRepository",
    "UbicacionRepository",
    "UsuarioRepository",
]