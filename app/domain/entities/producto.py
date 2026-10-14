"""Entidad de dominio: Producto."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(kw_only=True)
class Producto:
    """
    Producto del catálogo. NO almacena stock: el stock vive en la
    entidad Inventario (un producto puede estar en varias ubicaciones).
    """

    codigo: str
    nombre: str
    id: Optional[int] = None
    descripcion: Optional[str] = None
    categoria_id: Optional[int] = None
    unidad_medida: str = "pieza"
    stock_minimo: int = 0
    foto_url: Optional[str] = None
    activo: bool = True
    # Multialmacén: el catálogo pertenece a un almacén.
    almacen_id: int
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    def esta_activo(self) -> bool:
        return self.activo

    def requiere_alerta_por(self, stock_total: int) -> bool:
        """
        Determina si el stock total (sumando todas las ubicaciones)
        está por debajo del mínimo definido.
        """
        return stock_total < self.stock_minimo

    def validar(self) -> list[str]:
        """Validaciones básicas del producto. Devuelve lista de errores."""
        errores: list[str] = []
        if not self.codigo or not self.codigo.strip():
            errores.append("El código del producto es obligatorio")
        if not self.nombre or not self.nombre.strip():
            errores.append("El nombre del producto es obligatorio")
        if self.stock_minimo < 0:
            errores.append("El stock mínimo no puede ser negativo")
        return errores