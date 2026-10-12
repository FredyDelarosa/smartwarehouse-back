"""Casos de uso de inventario."""

from app.application.use_cases.inventario.alertas_stock_bajo import (
    AlertasStockBajoUseCase,
)
from app.application.use_cases.inventario.consultar_stock import (
    ConsultarStockUseCase,
)

__all__ = [
    "AlertasStockBajoUseCase",
    "ConsultarStockUseCase",
]