"""Modelo ORM: movimientos."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.entities.movimiento import TipoMovimiento
from app.infrastructure.database.base import Base

if TYPE_CHECKING:
    from app.infrastructure.database.models.producto_model import ProductoModel
    from app.infrastructure.database.models.ubicacion_model import UbicacionModel
    from app.infrastructure.database.models.usuario_model import UsuarioModel


class MovimientoModel(Base):
    __tablename__ = "movimientos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tipo: Mapped[TipoMovimiento] = mapped_column(
        SAEnum(
            TipoMovimiento,
            name="tipo_movimiento",
            native_enum=True,
            values_callable=lambda x: [e.value for e in x],
        ),
        nullable=False,
    )
    producto_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("productos.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    ubicacion_origen_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("ubicaciones.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
    )
    ubicacion_destino_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("ubicaciones.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
    )
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    usuario_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("usuarios.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    fecha: Mapped[Optional[datetime]] = mapped_column(
        DateTime, server_default=func.now(), nullable=True, index=True
    )
    referencia: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    observaciones: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relaciones
    producto: Mapped["ProductoModel"] = relationship(
        "ProductoModel",
        back_populates="movimientos",
        lazy="raise",
    )
    ubicacion_origen: Mapped[Optional["UbicacionModel"]] = relationship(
        "UbicacionModel",
        foreign_keys=[ubicacion_origen_id],
        back_populates="movimientos_origen",
        lazy="raise",
    )
    ubicacion_destino: Mapped[Optional["UbicacionModel"]] = relationship(
        "UbicacionModel",
        foreign_keys=[ubicacion_destino_id],
        back_populates="movimientos_destino",
        lazy="raise",
    )
    usuario: Mapped["UsuarioModel"] = relationship(
        "UsuarioModel",
        back_populates="movimientos",
        lazy="raise",
    )

    def __repr__(self) -> str:
        return (
            f"<MovimientoModel id={self.id} tipo={self.tipo} "
            f"producto_id={self.producto_id} cantidad={self.cantidad}>"
        )