"""
Excepciones de aplicación.
Son agnósticas al transporte: no saben nada de HTTP ni de FastAPI.
En la capa de infraestructura se mapean a códigos de estado HTTP.
"""

from typing import Any, Optional


class AppException(Exception):
    """Excepción base de la aplicación."""

    status_code: int = 500
    error_code: str = "INTERNAL_ERROR"
    message: str = "Error interno del servidor"

    def __init__(
        self,
        message: Optional[str] = None,
        *,
        error_code: Optional[str] = None,
        status_code: Optional[int] = None,
        details: Optional[Any] = None,
    ) -> None:
        self.message = message or self.message
        self.error_code = error_code or self.error_code
        self.status_code = status_code or self.status_code
        self.details = details
        super().__init__(self.message)

    def to_dict(self) -> dict:
        """Representación serializable para respuestas de error."""
        data: dict = {
            "error_code": self.error_code,
            "message": self.message,
        }
        if self.details is not None:
            data["details"] = self.details
        return data


# ============================================================
# 4xx - Errores del cliente
# ============================================================
class BadRequestError(AppException):
    status_code = 400
    error_code = "BAD_REQUEST"
    message = "Solicitud inválida"


class UnauthorizedError(AppException):
    status_code = 401
    error_code = "UNAUTHORIZED"
    message = "No autenticado"


class ForbiddenError(AppException):
    status_code = 403
    error_code = "FORBIDDEN"
    message = "No tiene permisos para realizar esta acción"


class NotFoundError(AppException):
    status_code = 404
    error_code = "NOT_FOUND"
    message = "Recurso no encontrado"


class ConflictError(AppException):
    status_code = 409
    error_code = "CONFLICT"
    message = "Conflicto con el estado actual del recurso"


class UnprocessableEntityError(AppException):
    status_code = 422
    error_code = "UNPROCESSABLE_ENTITY"
    message = "Entidad no procesable"


# ============================================================
# 5xx - Errores del servidor
# ============================================================
class InternalServerError(AppException):
    status_code = 500
    error_code = "INTERNAL_ERROR"
    message = "Error interno del servidor"