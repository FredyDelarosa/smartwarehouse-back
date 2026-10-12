"""Entidad de dominio: Ubicacion."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass(kw_only=True)
class Ubicacion:
    """
    Ubicación física dentro del almacén: pasillo + estante + nivel.

    El campo `codigo_ubicacion` sigue el formato 'P{pasillo}-{estante}-{nivel:02}',
    por ejemplo: 'P3-B-02'.
    """

    almacen_id: int
    pasillo: str
    estante: str
    nivel: str
    codigo_ubicacion: str
    id: Optional[int] = None
    codigo_qr: Optional[str] = None
    coordenada_x: Optional[Decimal] = None
    coordenada_y: Optional[Decimal] = None
    activo: bool = True
    created_at: Optional[datetime] = None

    def distancia_a(self, otra: "Ubicacion") -> Optional[float]:
        """
        Distancia euclidiana hasta otra ubicación usando coordenadas del mapa.
        Devuelve None si alguna de las dos ubicaciones no tiene coordenadas.
        """
        if (
            self.coordenada_x is None or self.coordenada_y is None
            or otra.coordenada_x is None or otra.coordenada_y is None
        ):
            return None
        dx = float(self.coordenada_x) - float(otra.coordenada_x)
        dy = float(self.coordenada_y) - float(otra.coordenada_y)
        return (dx * dx + dy * dy) ** 0.5

    def misma_ubicacion_fisica(self, otra: "Ubicacion") -> bool:
        """True si ambas comparten almacén, pasillo, estante y nivel."""
        return (
            self.almacen_id == otra.almacen_id
            and self.pasillo == otra.pasillo
            and self.estante == otra.estante
            and self.nivel == otra.nivel
        )