"""Modelo ORM: busquedas."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base

if TYPE_CHECKING:
    from app.infrastructure.database.models.producto_model import ProductoModel
    from app.infrastructure.database.models.ubicacion_model import UbicacionModel
    from app.infrastructure.database.models.usuario_model import UsuarioModel


class BusquedaModel(Base):
    __tablename__ = "busquedas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("usuarios.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    producto_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("productos.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    termino_busqueda: Mapped[str] = mapped_column(String(150), nullable=False)
    fecha_hora_inicio: Mapped[Optional[datetime]] = mapped_column(
        DateTime, server_default=func.now(), nullable=True, index=True
    )
    fecha_hora_fin: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    tiempo_busqueda_segundos: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True
    )
    ubicacion_encontrada_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("ubicaciones.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
    )
    exito: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    observaciones: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relaciones
    usuario: Mapped["UsuarioModel"] = relationship(
        "UsuarioModel",
        back_populates="busquedas",
        lazy="raise",
    )
    producto: Mapped[Optional["ProductoModel"]] = relationship(
        "ProductoModel",
        back_populates="busquedas",
        lazy="raise",
    )
    ubicacion_encontrada: Mapped[Optional["UbicacionModel"]] = relationship(
        "UbicacionModel",
        lazy="raise",
    )

    def __repr__(self) -> str:
        return (
            f"<BusquedaModel id={self.id} termino={self.termino_busqueda!r} "
            f"tiempo={self.tiempo_busqueda_segundos}s exito={self.exito}>"
        )