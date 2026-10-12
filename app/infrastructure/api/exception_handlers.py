"""
Manejadores globales de excepciones.
Traducen excepciones del dominio y de la aplicación a respuestas HTTP.
"""

from __future__ import annotations

import logging

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions import AppException
from app.domain.exceptions import (
    CredencialesInvalidasError,
    DomainError,
    EntidadDuplicadaError,
    EntidadNoEncontradaError,
    StockInsuficienteError,
    UsuarioInactivoError,
    ValidacionError,
)

logger = logging.getLogger("smartwarehouse.errors")


# ============================================================
# Mapa tipo de excepción de dominio → código HTTP
# El orden importa: el primero que matchee gana.
# Se evalúa de más específico a más genérico.
# ============================================================
_DOMAIN_STATUS_MAP: list[tuple[type[DomainError], int]] = [
    (CredencialesInvalidasError, 401),
    (UsuarioInactivoError, 403),
    (EntidadNoEncontradaError, 404),
    (EntidadDuplicadaError, 409),
    (StockInsuficienteError, 409),
    (ValidacionError, 422),
]


def _status_for_domain_error(exc: DomainError) -> int:
    for exc_type, status in _DOMAIN_STATUS_MAP:
        if isinstance(exc, exc_type):
            return status
    return 400  # DomainError genérica


# ============================================================
# Handlers
# ============================================================
async def app_exception_handler(
    request: Request, exc: AppException
) -> JSONResponse:
    """Excepciones de la capa `core` (ya traen status_code propio)."""
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict(),
    )


async def domain_exception_handler(
    request: Request, exc: DomainError
) -> JSONResponse:
    """Excepciones del dominio: se mapean a HTTP aquí."""
    status = _status_for_domain_error(exc)
    return JSONResponse(
        status_code=status,
        content={
            "error_code": exc.code,
            "message": exc.message,
            "details": jsonable_encoder(exc.details) if exc.details else None,
        },
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Errores de validación de Pydantic en el body/query/path."""
    return JSONResponse(
        status_code=422,
        content={
            "error_code": "REQUEST_VALIDATION_ERROR",
            "message": "Datos de entrada inválidos",
            "details": {"errors": jsonable_encoder(exc.errors())},
        },
    )


async def unhandled_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """Fallback para cualquier excepción no controlada."""
    logger.exception("Excepción no controlada en %s %s", request.method, request.url)
    return JSONResponse(
        status_code=500,
        content={
            "error_code": "INTERNAL_ERROR",
            "message": "Error interno del servidor",
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Registra todos los handlers en la app de FastAPI."""
    app.add_exception_handler(AppException, app_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(DomainError, domain_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, unhandled_exception_handler)