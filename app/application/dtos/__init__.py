"""
DTOs (Data Transfer Objects) de la capa de aplicación.
Re-exporta todos los esquemas para imports limpios.
"""

from app.application.dtos.almacen_dto import (
    AlmacenBaseDTO,
    AlmacenCreateDTO,
    AlmacenReadDTO,
    AlmacenUpdateDTO,
)
from app.application.dtos.auth_dto import (
    ChangePasswordDTO,
    LoginDTO,
    RefreshTokenDTO,
    TokenDTO,
    TokenPayloadDTO,
)
from app.application.dtos.busqueda_dto import (
    BusquedaFinalizadaDTO,
    BusquedaReadDTO,
    FinalizarBusquedaDTO,
    IniciarBusquedaDTO,
    ResultadoBusquedaDTO,
    UbicacionConStockDTO,
)
from app.application.dtos.categoria_dto import (
    CategoriaBaseDTO,
    CategoriaCreateDTO,
    CategoriaReadDTO,
    CategoriaUpdateDTO,
)
from app.application.dtos.incidencia_dto import (
    IncidenciaCreateDTO,
    IncidenciaReadDTO,
    IncidenciaUpdateDTO,
)
from app.application.dtos.inventario_dto import (
    InventarioBaseDTO,
    InventarioCreateDTO,
    InventarioReadDTO,
    InventarioUpdateDTO,
    ProductoEnUbicacionResumenDTO,
    StockPorUbicacionDTO,
    UbicacionStockDTO,
    StockTotalProductoDTO,
)
from app.application.dtos.metricas_dto import (
    ComparativaBusquedaDTO,
    DashboardResumenDTO,
    ProductoStockBajoDTO,
    RangoFechasDTO,
    ResumenIncidenciasDTO,
    ResumenMovimientosDTO,
    TiempoPromedioBusquedaDTO,
)
from app.application.dtos.movimiento_dto import (
    MovimientoBaseDTO,
    MovimientoCreateDTO,
    MovimientoReadDTO,
)
from app.application.dtos.producto_dto import (
    ProductoBaseDTO,
    ProductoCreateDTO,
    ProductoReadDTO,
    ProductoSearchDTO,
    ProductoUpdateDTO,
)
from app.application.dtos.ubicacion_dto import (
    ProductoEnUbicacionDTO,
    UbicacionBaseDTO,
    UbicacionCreateDTO,
    UbicacionQRReadDTO,
    UbicacionReadDTO,
    UbicacionUpdateDTO,
)
from app.application.dtos.usuario_dto import (
    UsuarioBaseDTO,
    UsuarioCreateDTO,
    UsuarioReadDTO,
    UsuarioUpdateDTO,
)

# Resolver referencias diferidas (forward refs) usadas en UbicacionQRReadDTO
UbicacionQRReadDTO.model_rebuild()
ResultadoBusquedaDTO.model_rebuild()

__all__ = [
    # Almacen
    "AlmacenBaseDTO", "AlmacenCreateDTO", "AlmacenReadDTO", "AlmacenUpdateDTO",
    # Auth
    "ChangePasswordDTO", "LoginDTO", "RefreshTokenDTO", "TokenDTO", "TokenPayloadDTO",
    # Busqueda
    "BusquedaFinalizadaDTO", "BusquedaReadDTO", "FinalizarBusquedaDTO", "IniciarBusquedaDTO",
    "ResultadoBusquedaDTO", "UbicacionConStockDTO",
    # Categoria
    "CategoriaBaseDTO", "CategoriaCreateDTO", "CategoriaReadDTO", "CategoriaUpdateDTO",
    # Incidencia
    "IncidenciaCreateDTO", "IncidenciaReadDTO", "IncidenciaUpdateDTO",
    # Inventario
    "InventarioBaseDTO", "InventarioCreateDTO", "InventarioReadDTO",
    "InventarioUpdateDTO", "StockPorUbicacionDTO", "StockTotalProductoDTO",
    # Metricas
    "ComparativaBusquedaDTO", "DashboardResumenDTO", "ProductoStockBajoDTO",
    "RangoFechasDTO", "ResumenIncidenciasDTO", "ResumenMovimientosDTO",
    "TiempoPromedioBusquedaDTO",
    # Movimiento
    "MovimientoBaseDTO", "MovimientoCreateDTO", "MovimientoReadDTO",
    # Producto
    "ProductoBaseDTO", "ProductoCreateDTO", "ProductoReadDTO",
    "ProductoSearchDTO", "ProductoUpdateDTO",
    # Ubicacion
    "ProductoEnUbicacionDTO", "UbicacionBaseDTO", "UbicacionCreateDTO",
    "UbicacionQRReadDTO", "UbicacionReadDTO", "UbicacionUpdateDTO",
    # Usuario
    "UsuarioBaseDTO", "UsuarioCreateDTO", "UsuarioReadDTO", "UsuarioUpdateDTO",
]