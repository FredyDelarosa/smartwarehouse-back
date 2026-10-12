"""Entidad de dominio: Inventario."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(kw_only=True)
class Inventario:
    """
    Stock de UN producto en UNA ubicación concreta.
    La cantidad total de un producto = SUM(inventario.cantidad) para ese producto.
    """

    producto_id: int
    ubicacion_id: int
    cantidad: int = 0
    id: Optional[int] = None
    fecha_actualizacion: Optional[datetime] = None

    def esta_vacio(self) -> bool:
        return self.cantidad == 0

    def incrementar(self, cantidad: int) -> None:
        """Suma unidades al stock actual."""
        if cantidad <= 0:
            raise ValueError("La cantidad a incrementar debe ser positiva")
        self.cantidad += cantidad

    def decrementar(self, cantidad: int) -> None:
        """
        Resta unidades al stock actual.
        Lanza ValueError si la cantidad es inválida o si no hay stock suficiente.
        """
        if cantidad <= 0:
            raise ValueError("La cantidad a decrementar debe ser positiva")
        if cantidad > self.cantidad:
            raise ValueError(
                f"Stock insuficiente: disponible {self.cantidad}, "
                f"solicitado {cantidad}"
            )
        self.cantidad -= cantidad

    def ajustar(self, nueva_cantidad: int) -> None:
        """Ajusta el stock a un valor absoluto (usado en conteos físicos)."""
        if nueva_cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")
        self.cantidad = nueva_cantidad