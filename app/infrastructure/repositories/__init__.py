"""Implementaciones concretas de los puertos de repositorio."""

from app.infrastructure.repositories.almacen_repository_impl import (
    AlmacenRepositoryImpl,
)
from app.infrastructure.repositories.busqueda_repository_impl import (
    BusquedaRepositoryImpl,
)
from app.infrastructure.repositories.categoria_repository_impl import (
    CategoriaRepositoryImpl,
)
from app.infrastructure.repositories.incidencia_repository_impl import (
    IncidenciaRepositoryImpl,
)
from app.infrastructure.repositories.inventario_repository_impl import (
    InventarioRepositoryImpl,
)
from app.infrastructure.repositories.movimiento_repository_impl import (
    MovimientoRepositoryImpl,
)
from app.infrastructure.repositories.producto_repository_impl import (
    ProductoRepositoryImpl,
)
from app.infrastructure.repositories.rol_repository_impl import (
    RolRepositoryImpl,
)
from app.infrastructure.repositories.ubicacion_repository_impl import (
    UbicacionRepositoryImpl,
)
from app.infrastructure.repositories.usuario_repository_impl import (
    UsuarioRepositoryImpl,
)

__all__ = [
    "AlmacenRepositoryImpl",
    "BusquedaRepositoryImpl",
    "CategoriaRepositoryImpl",
    "IncidenciaRepositoryImpl",
    "InventarioRepositoryImpl",
    "MovimientoRepositoryImpl",
    "ProductoRepositoryImpl",
    "RolRepositoryImpl",
    "UbicacionRepositoryImpl",
    "UsuarioRepositoryImpl",
]