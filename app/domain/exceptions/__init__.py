"""
Excepciones del dominio.
Re-exporta todas las clases para imports limpios.
"""

from app.domain.exceptions.domain_exceptions import (
    # Base
    DomainError,
    # Genéricas
    EntidadNoEncontradaError,
    EntidadDuplicadaError,
    ValidacionError,
    # Usuarios / Auth
    UsuarioNoEncontradoError,
    CredencialesInvalidasError,
    UsuarioInactivoError,
    EmailYaRegistradoError,
    # Productos
    ProductoNoEncontradoError,
    CodigoProductoDuplicadoError,
    # Ubicaciones
    UbicacionNoEncontradaError,
    UbicacionDuplicadaError,
    CodigoUbicacionInvalidoError,
    # Inventario
    StockInsuficienteError,
    InventarioNoEncontradoError,
    CantidadInvalidaError,
    # Movimientos
    MovimientoInvalidoError,
    # Incidencias
    IncidenciaNoEncontradaError,
    # Búsquedas
    BusquedaNoEncontradaError,
    # Categorías
    CategoriaNoEncontradaError,
)

__all__ = [
    "DomainError",
    "EntidadNoEncontradaError",
    "EntidadDuplicadaError",
    "ValidacionError",
    "UsuarioNoEncontradoError",
    "CredencialesInvalidasError",
    "UsuarioInactivoError",
    "EmailYaRegistradoError",
    "ProductoNoEncontradoError",
    "CodigoProductoDuplicadoError",
    "UbicacionNoEncontradaError",
    "UbicacionDuplicadaError",
    "CodigoUbicacionInvalidoError",
    "StockInsuficienteError",
    "InventarioNoEncontradoError",
    "CantidadInvalidaError",
    "MovimientoInvalidoError",
    "IncidenciaNoEncontradaError",
    "BusquedaNoEncontradaError",
    "CategoriaNoEncontradaError",
]