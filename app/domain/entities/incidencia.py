"""Entidad de dominio: Incidencia."""

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class TipoIncidencia(str, Enum):
    """Tipos de incidencia soportados."""

    MAL_UBICADO = "MAL_UBICADO"
    FALTANTE = "FALTANTE"
    DANADO = "DANADO"
    OTRO = "OTRO"


@dataclass(kw_only=True)
class Incidencia:
    """
    Reporte de una incidencia del almacén: producto mal ubicado,
    faltante, dañado o cualquier otro evento.
    """

    tipo: TipoIncidencia
    usuario_id: int
    id: Optional[int] = None
    producto_id: Optional[int] = None
    ubicacion_id: Optional[int] = None
    fecha: Optional[datetime] = None
    descripcion: Optional[str] = None
    resuelta: bool = False
    fecha_resolucion: Optional[datetime] = None

    def resolver(self) -> None:
        """Marca la incidencia como resuelta con la fecha/hora actual (UTC naive)."""
        self.resuelta = True
        self.fecha_resolucion = datetime.utcnow()

    def esta_abierta(self) -> bool:
        return not self.resuelta