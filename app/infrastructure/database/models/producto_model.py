"""Modelo ORM: productos."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base

if TYPE_CHECKING:
    from app.infrastructure.database.models.busqueda_model import BusquedaModel
    from app.infrastructure.database.models.categoria_model import CategoriaModel
    from app.infrastructure.database.models.incidencia_model import IncidenciaModel
    from app.infrastructure.database.models.inventario_model import InventarioModel
    from app.infrastructure.database.models.movimiento_model import MovimientoModel


class ProductoModel(Base):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    categoria_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("categorias.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
    )
    unidad_medida: Mapped[str] = mapped_column(
        String(20), default="pieza", nullable=False
    )
    stock_minimo: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    foto_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    fecha_creacion: Mapped[Optional[datetime]] = mapped_column(
        DateTime, server_default=func.now(), nullable=True
    )
    fecha_actualizacion: Mapped[Optional[datetime]] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=True
    )

    # Relaciones
    categoria: Mapped[Optional["CategoriaModel"]] = relationship(
        "CategoriaModel",
        back_populates="productos",
        lazy="raise",
    )
    inventarios: Mapped[List["InventarioModel"]] = relationship(
        "InventarioModel",
        back_populates="producto",
        lazy="raise",
    )
    movimientos: Mapped[List["MovimientoModel"]] = relationship(
        "MovimientoModel",
        back_populates="producto",
        lazy="raise",
    )
    busquedas: Mapped[List["BusquedaModel"]] = relationship(
        "BusquedaModel",
        back_populates="producto",
        lazy="raise",
    )
    incidencias: Mapped[List["IncidenciaModel"]] = relationship(
        "IncidenciaModel",
        back_populates="producto",
        lazy="raise",
    )

    def __repr__(self) -> str:
        return f"<ProductoModel id={self.id} codigo={self.codigo!r}>"