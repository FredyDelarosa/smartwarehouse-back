"""Entidad de dominio: Movimiento."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class TipoMovimiento(str, Enum):
    """Tipos de movimiento soportados por el sistema."""

    ENTRADA = "ENTRADA"
    SALIDA = "SALIDA"
    TRASLADO = "TRASLADO"
    AJUSTE = "AJUSTE"


@dataclass(kw_only=True)
class Movimiento:
    """
    Registro histórico de un movimiento de inventario.
    Una entrada o salida afecta una sola ubicación.
    Un traslado afecta dos ubicaciones (origen y destino).
    """

    tipo: TipoMovimiento
    producto_id: int
    cantidad: int
    usuario_id: int
    id: Optional[int] = None
    ubicacion_origen_id: Optional[int] = None
    ubicacion_destino_id: Optional[int] = None
    fecha: Optional[datetime] = None
    referencia: Optional[str] = None
    observaciones: Optional[str] = None

    # ----- Helpers de tipo -----
    def es_entrada(self) -> bool:
        return self.tipo == TipoMovimiento.ENTRADA

    def es_salida(self) -> bool:
        return self.tipo == TipoMovimiento.SALIDA

    def es_traslado(self) -> bool:
        return self.tipo == TipoMovimiento.TRASLADO

    def es_ajuste(self) -> bool:
        return self.tipo == TipoMovimiento.AJUSTE

    # ----- Validaciones -----
    def validar(self) -> list[str]:
        """
        Devuelve una lista de errores según las reglas del tipo de movimiento.
        Lista vacía => movimiento válido.
        """
        errores: list[str] = []

        if self.cantidad <= 0:
            errores.append("La cantidad debe ser mayor que cero")
        if self.producto_id is None:
            errores.append("El producto es obligatorio")
        if self.usuario_id is None:
            errores.append("El usuario es obligatorio")

        if self.es_entrada() and self.ubicacion_destino_id is None:
            errores.append("Una ENTRADA requiere ubicación destino")

        if self.es_salida() and self.ubicacion_origen_id is None:
            errores.append("Una SALIDA requiere ubicación origen")

        if self.es_traslado():
            if self.ubicacion_origen_id is None:
                errores.append("Un TRASLADO requiere ubicación origen")
            if self.ubicacion_destino_id is None:
                errores.append("Un TRASLADO requiere ubicación destino")
            if (
                self.ubicacion_origen_id is not None
                and self.ubicacion_origen_id == self.ubicacion_destino_id
            ):
                errores.append(
                    "El origen y el destino de un TRASLADO no pueden ser iguales"
                )

        if self.es_ajuste() and (
            self.ubicacion_origen_id is None
            and self.ubicacion_destino_id is None
        ):
            errores.append("Un AJUSTE requiere ubicación afectada")

        return errores