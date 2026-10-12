"""Entidad de dominio: Busqueda."""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass(kw_only=True)
class Busqueda:
    """
    Registro de una búsqueda de producto.
    Sirve para medir tiempos de localización (indicador clave del proyecto).

    Nota sobre fechas: trabajamos con `datetime` naive en UTC porque
    MySQL DATETIME no almacena zona horaria. Las comparaciones se hacen
    siempre en ese espacio, sin mezclar aware/naive.
    """

    usuario_id: int
    termino_busqueda: str
    id: Optional[int] = None
    producto_id: Optional[int] = None
    producto_nombre: Optional[str] = None
    fecha_hora_inicio: Optional[datetime] = None
    fecha_hora_fin: Optional[datetime] = None
    tiempo_busqueda_segundos: Optional[int] = None
    ubicacion_encontrada_id: Optional[int] = None
    exito: bool = False
    observaciones: Optional[str] = None

    def iniciar(self) -> None:
        """Marca el inicio de la búsqueda con la hora actual (UTC naive)."""
        self.fecha_hora_inicio = datetime.utcnow()
        self.exito = False

    def finalizar(
        self,
        ubicacion_encontrada_id: Optional[int] = None,
        observaciones: Optional[str] = None,
    ) -> None:
        """
        Cierra la búsqueda: calcula tiempo y marca éxito.
        Éxito = se encontró una ubicación.

        Si `fecha_hora_inicio` viniera con tzinfo (por ejemplo, si un
        cliente externo la fijó con zona horaria), se normaliza a UTC naive
        antes de calcular la diferencia.
        """
        ahora = datetime.utcnow()
        self.fecha_hora_fin = ahora

        if self.fecha_hora_inicio is not None:
            inicio = self.fecha_hora_inicio
            if inicio.tzinfo is not None:
                # Convertir a UTC y quitar tzinfo para que sea naive
                inicio = inicio.astimezone(timezone.utc).replace(tzinfo=None)
            delta = ahora - inicio
            self.tiempo_busqueda_segundos = max(0, int(delta.total_seconds()))

        self.ubicacion_encontrada_id = ubicacion_encontrada_id
        self.exito = ubicacion_encontrada_id is not None
        if observaciones:
            self.observaciones = observaciones

    def tiempo_en_minutos(self) -> Optional[float]:
        """Tiempo de búsqueda expresado en minutos."""
        if self.tiempo_busqueda_segundos is None:
            return None
        return round(self.tiempo_busqueda_segundos / 60.0, 2)