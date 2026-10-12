"""
Excepciones del dominio.

Son agnósticas a cualquier framework: no conocen HTTP, ni FastAPI,
ni SQLAlchemy. Solo representan reglas de negocio violadas.

En la capa de infraestructura se mapean a las excepciones de
aplicación definidas en `app.core.exceptions`.
"""

from typing import Any, Optional


# ============================================================
# Base
# ============================================================
class DomainError(Exception):
    """
    Excepción base del dominio.

    Todas las excepciones de negocio heredan de aquí para poder
    capturarlas de forma genérica si hiciera falta.
    """

    code: str = "DOMAIN_ERROR"
    default_message: str = "Error de dominio"

    def __init__(
        self,
        message: Optional[str] = None,
        *,
        details: Optional[Any] = None,
    ) -> None:
        self.message = message or self.default_message
        self.details = details
        super().__init__(self.message)

    def to_dict(self) -> dict:
        """Representación serializable para logs y respuestas."""
        data: dict = {"code": self.code, "message": self.message}
        if self.details is not None:
            data["details"] = self.details
        return data

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(message={self.message!r}, details={self.details!r})"


# ============================================================
# Genéricas
# ============================================================
class EntidadNoEncontradaError(DomainError):
    """Se lanza cuando se busca una entidad que no existe."""

    code = "ENTIDAD_NO_ENCONTRADA"
    default_message = "La entidad solicitada no existe"


class EntidadDuplicadaError(DomainError):
    """Se lanza al intentar crear algo que ya existe (por clave única)."""

    code = "ENTIDAD_DUPLICADA"
    default_message = "Ya existe una entidad con esos datos"


class ValidacionError(DomainError):
    """Se lanza cuando los datos de una entidad no cumplen las reglas de negocio."""

    code = "VALIDACION_FALLIDA"
    default_message = "Los datos no cumplen las reglas de negocio"

    def __init__(
        self,
        message: Optional[str] = None,
        *,
        errores: Optional[list[str]] = None,
    ) -> None:
        super().__init__(
            message=message,
            details={"errores": errores} if errores else None,
        )
        self.errores = errores or []


# ============================================================
# Usuarios y autenticación
# ============================================================
class UsuarioNoEncontradoError(EntidadNoEncontradaError):
    code = "USUARIO_NO_ENCONTRADO"
    default_message = "Usuario no encontrado"


class CredencialesInvalidasError(DomainError):
    code = "CREDENCIALES_INVALIDAS"
    default_message = "Credenciales inválidas"


class UsuarioInactivoError(DomainError):
    code = "USUARIO_INACTIVO"
    default_message = "El usuario está inactivo y no puede autenticarse"


class EmailYaRegistradoError(EntidadDuplicadaError):
    code = "EMAIL_YA_REGISTRADO"
    default_message = "El correo electrónico ya está registrado"


# ============================================================
# Productos
# ============================================================
class ProductoNoEncontradoError(EntidadNoEncontradaError):
    code = "PRODUCTO_NO_ENCONTRADO"
    default_message = "Producto no encontrado"


class CodigoProductoDuplicadoError(EntidadDuplicadaError):
    code = "CODIGO_PRODUCTO_DUPLICADO"
    default_message = "Ya existe un producto con ese código"


# ============================================================
# Ubicaciones
# ============================================================
class UbicacionNoEncontradaError(EntidadNoEncontradaError):
    code = "UBICACION_NO_ENCONTRADA"
    default_message = "Ubicación no encontrada"


class UbicacionDuplicadaError(EntidadDuplicadaError):
    code = "UBICACION_DUPLICADA"
    default_message = "Ya existe una ubicación con ese código"


class CodigoUbicacionInvalidoError(ValidacionError):
    code = "CODIGO_UBICACION_INVALIDO"
    default_message = "El código de ubicación no tiene un formato válido"


# ============================================================
# Inventario y stock
# ============================================================
class StockInsuficienteError(DomainError):
    code = "STOCK_INSUFICIENTE"
    default_message = "No hay suficiente stock para realizar la operación"

    def __init__(
        self,
        message: Optional[str] = None,
        *,
        disponible: Optional[int] = None,
        solicitado: Optional[int] = None,
    ) -> None:
        detalles: dict = {}
        if disponible is not None:
            detalles["disponible"] = disponible
        if solicitado is not None:
            detalles["solicitado"] = solicitado
        super().__init__(
            message=message or self.default_message,
            details=detalles or None,
        )
        self.disponible = disponible
        self.solicitado = solicitado


class InventarioNoEncontradoError(EntidadNoEncontradaError):
    code = "INVENTARIO_NO_ENCONTRADO"
    default_message = "No hay registro de inventario para ese producto en esa ubicación"


class CantidadInvalidaError(ValidacionError):
    code = "CANTIDAD_INVALIDA"
    default_message = "La cantidad indicada no es válida"


# ============================================================
# Movimientos
# ============================================================
class MovimientoInvalidoError(ValidacionError):
    code = "MOVIMIENTO_INVALIDO"
    default_message = "El movimiento no cumple las reglas de negocio"


# ============================================================
# Incidencias
# ============================================================
class IncidenciaNoEncontradaError(EntidadNoEncontradaError):
    code = "INCIDENCIA_NO_ENCONTRADA"
    default_message = "Incidencia no encontrada"


# ============================================================
# Búsquedas
# ============================================================
class BusquedaNoEncontradaError(EntidadNoEncontradaError):
    code = "BUSQUEDA_NO_ENCONTRADA"
    default_message = "Búsqueda no encontrada"


# ============================================================
# Categorías
# ============================================================
class CategoriaNoEncontradaError(EntidadNoEncontradaError):
    code = "CATEGORIA_NO_ENCONTRADA"
    default_message = "Categoría no encontrada"