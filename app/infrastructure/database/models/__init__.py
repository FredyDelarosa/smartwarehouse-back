"""
Re-exporta todos los modelos ORM.
Importar este paquete registra los modelos en `Base.metadata`,
lo cual es requisito para Alembic y para `create_all`.
"""

from app.infrastructure.database.models.almacen_model import AlmacenModel
from app.infrastructure.database.models.busqueda_model import BusquedaModel
from app.infrastructure.database.models.categoria_model import CategoriaModel
from app.infrastructure.database.models.incidencia_model import IncidenciaModel
from app.infrastructure.database.models.inventario_model import InventarioModel
from app.infrastructure.database.models.movimiento_model import MovimientoModel
from app.infrastructure.database.models.producto_model import ProductoModel
from app.infrastructure.database.models.rol_model import RolModel
from app.infrastructure.database.models.ubicacion_model import UbicacionModel
from app.infrastructure.database.models.usuario_model import UsuarioModel

__all__ = [
    "AlmacenModel",
    "BusquedaModel",
    "CategoriaModel",
    "IncidenciaModel",
    "InventarioModel",
    "MovimientoModel",
    "ProductoModel",
    "RolModel",
    "UbicacionModel",
    "UsuarioModel",
]