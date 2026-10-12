"""DTOs: Métricas e indicadores."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.domain.entities import TipoIncidencia, TipoMovimiento


class RangoFechasDTO(BaseModel):
    desde: Optional[datetime] = None
    hasta: Optional[datetime] = None


class TiempoPromedioBusquedaDTO(BaseModel):
    desde: Optional[datetime] = None
    hasta: Optional[datetime] = None
    total_busquedas: int
    promedio_segundos: Optional[float] = None
    promedio_minutos: Optional[float] = None
    exitosas: int = 0
    fallidas: int = 0


class ComparativaBusquedaDTO(BaseModel):
    """
    Compara dos periodos para demostrar mejora.
    Ej: julio (517s) vs septiembre (82s) → mejora 84%.
    """

    periodo_actual: TiempoPromedioBusquedaDTO
    periodo_anterior: TiempoPromedioBusquedaDTO
    mejora_segundos: Optional[float] = None
    mejora_porcentaje: Optional[float] = None


class ProductoStockBajoDTO(BaseModel):
    producto_id: int
    codigo: str
    nombre: str
    unidad_medida: str
    stock_total: int
    stock_minimo: int
    faltante: int = Field(..., description="Cuánto falta para llegar al mínimo")


class ResumenIncidenciasDTO(BaseModel):
    total: int
    abiertas: int
    resueltas: int
    por_tipo: dict[TipoIncidencia, int]


class ResumenMovimientosDTO(BaseModel):
    total: int
    por_tipo: dict[TipoMovimiento, int]
    total_piezas_movidas: int


class DashboardResumenDTO(BaseModel):
    """Vista agregada de los indicadores principales."""

    total_productos: int
    total_ubicaciones: int
    productos_stock_bajo: int
    total_incidencias_abiertas: int
    tiempo_promedio_busqueda_segundos: Optional[float] = None
    tiempo_promedio_busqueda_minutos: Optional[float] = None
    total_busquedas: int