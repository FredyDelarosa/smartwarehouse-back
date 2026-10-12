"""Modelo ORM: inventario."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base

if TYPE_CHECKING:
    from app.infrastructure.database.models.producto_model import ProductoModel
    from app.infrastructure.database.models.ubicacion_model import UbicacionModel


class InventarioModel(Base):
    __tablename__ = "inventario"
    __table_args__ = (
        UniqueConstraint(
            "producto_id", "ubicacion_id",
            name="uk_inventario_producto_ubicacion",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    producto_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("productos.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    ubicacion_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("ubicaciones.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    cantidad: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    fecha_actualizacion: Mapped[Optional[datetime]] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=True
    )

    # Relaciones
    producto: Mapped["ProductoModel"] = relationship(
        "ProductoModel",
        back_populates="inventarios",
        lazy="raise",
    )
    ubicacion: Mapped["UbicacionModel"] = relationship(
        "UbicacionModel",
        back_populates="inventarios",
        lazy="raise",
    )

    def __repr__(self) -> str:
        return (
            f"<InventarioModel id={self.id} producto_id={self.producto_id} "
            f"ubicacion_id={self.ubicacion_id} cantidad={self.cantidad}>"
        )